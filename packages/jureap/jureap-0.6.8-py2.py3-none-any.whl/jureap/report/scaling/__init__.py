# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import itertools
import os
import tempfile
import shutil
import subprocess
import json
import sys
import matplotlib.pyplot
import math
import numpy


def prepare_plotting_data(experiment_array):
    complete_plotting_data = {}
    complete_plotting_data["experiment"] = []

    for experiment in experiment_array:
        plotting_data = {}
        plotting_data["pipeline"] = experiment.pipeline()
        plotting_data["workload_factor"] = float(experiment.workload_factor())
        plotting_data["runtime"] = {}
        plotting_data["runtime"]["nodes"] = []
        plotting_data["runtime"]["runtime"] = []
        for data in experiment.json_data()["data"]:
            plotting_data["runtime"]["nodes"].append(int(data["parameter"]["nodes"]))
            plotting_data["runtime"]["runtime"].append(float(data["runtime"]))

            plotting_data["runtime"]["runtime"] = [
                x
                for _, x in sorted(
                    zip(plotting_data["runtime"]["nodes"], plotting_data["runtime"]["runtime"])
                )
            ]

            plotting_data["runtime"]["nodes"] = sorted(plotting_data["runtime"]["nodes"])

        plotting_data["label"] = experiment.prefix()

        complete_plotting_data["experiment"].append(plotting_data)

    min_nodes = sys.maxsize
    max_nodes = 0
    min_runtime = sys.float_info.max
    max_runtime = 0

    max_workload_factor = sys.float_info.max

    for pipeline_data in complete_plotting_data["experiment"]:
        local_max = max(pipeline_data["runtime"]["nodes"])
        local_min = min(pipeline_data["runtime"]["nodes"])
        min_nodes = min(min_nodes, local_min)
        max_nodes = max(max_nodes, local_max)
        local_max = max(pipeline_data["runtime"]["runtime"])
        local_min = min(pipeline_data["runtime"]["runtime"])
        min_runtime = min(min_runtime, local_min)
        max_runtime = max(max_runtime, local_max)

    complete_plotting_data["node_range"] = [0.5 * min_nodes, 1.4 * max_nodes]
    complete_plotting_data["runtime_range"] = [0.5 * min_runtime, 1.4 * max_runtime]

    workload_factor_array = [
        data["workload_factor"] for data in complete_plotting_data["experiment"]
    ]
    min_workload_factor = min(workload_factor_array)
    normalized_wf = [p / min_workload_factor for p in workload_factor_array]

    base_runtime = 0
    for index, pipeline_data in enumerate(complete_plotting_data["experiment"]):
        if min(pipeline_data["runtime"]["nodes"]) == min_nodes:

            min_node_index = min(
                range(len(pipeline_data["runtime"]["nodes"])),
                key=pipeline_data["runtime"]["nodes"].__getitem__,
            )


            base_runtime = pipeline_data["runtime"]["runtime"][min_node_index]

    for index, pipeline_data in enumerate(complete_plotting_data["experiment"]):
        pipeline_data["expected_runtime"] = {}
        pipeline_data["expected_runtime"]["nodes"] = pipeline_data["runtime"]["nodes"]
        pipeline_data["expected_runtime"]["runtime"] = [
            normalized_wf[index] * base_runtime / p * min_nodes
            for p in pipeline_data["runtime"]["nodes"]
        ]

    complete_plotting_data["base_runtime"] = base_runtime

    return complete_plotting_data


def generate_plot_pdf_file(plotting_data, output_dir):
    plot = matplotlib.pyplot.figure()
    marker = itertools.cycle(("o","^","s","d","X"))

    ax = plot.subplots()
    ax.set_xlabel("Number of Nodes (log-scale)")
    ax.set_ylabel("runtime / s (log-scale)")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.margins(2)

    range_limits = {}
    range_limits["xlim"] = plotting_data["node_range"]
    range_limits["ylim"] = plotting_data["runtime_range"]
    if math.log(range_limits["ylim"][0]) < 0 or math.log(range_limits["ylim"][1]) < 0:
        range_limits["yticks"] = numpy.linspace(
            range_limits["ylim"][0], range_limits["ylim"][1], num=8
        )
    else:
        range_limits["yticks"] = numpy.logspace(
            math.log(range_limits["ylim"][0], 2),
            math.log(range_limits["ylim"][1], 2),
            num=8,
            base=2,
        )
        range_limits["yticks"] = [int(p) for p in range_limits["yticks"]]

    ax.set_yticks(range_limits["yticks"])
    ax.set_yticklabels(range_limits["yticks"])

    cmap = matplotlib.colormaps["tab10"]

    xticklabels = []
    colorgen = iter([cmap(i) for i in range(10)])
    ax.grid(visible=True, which="major", axis="x", linestyle="-", linewidth=0.5, alpha=0.5)

    for pipeline_data in plotting_data["experiment"]:
        xticklabels = xticklabels + pipeline_data["runtime"]["nodes"]
        color = next(colorgen)
        xaxis_data = pipeline_data["runtime"]["nodes"]
        yaxis_data = pipeline_data["runtime"]["runtime"]

        ideal_scaling_array = []
        low_scaling_array = []
        for i in range(len(xaxis_data)):
            ideal_scaling = yaxis_data[0] / xaxis_data[i] * xaxis_data[0]
            low_scaling = ideal_scaling * 1.25
            ideal_scaling_array.append(ideal_scaling)
            low_scaling_array.append(low_scaling)

        label = pipeline_data["label"]
        prefix = pipeline_data["pipeline"]
        ax.plot(xaxis_data, yaxis_data, label=label, marker=next(marker), color=color, markersize=4)
        ax.fill_between(
            xaxis_data, ideal_scaling_array, low_scaling_array, color=color, alpha=0.1, ls="--"
        )

        if float(pipeline_data["workload_factor"]) > 1:
            expected_yaxis = pipeline_data["expected_runtime"]["runtime"]
            error_yaxis_positive = [0.25 * i for i in expected_yaxis]
            error_yaxis_negative = [0 for p in expected_yaxis]
            error_absolute_positive = [1.25 * i for i in expected_yaxis]
            error_absolute_negative = [0.75 * i for i in expected_yaxis]

            min_error_absolute = min(error_absolute_negative)
            max_error_absolute = max(error_absolute_positive)

            if range_limits["ylim"][0] > min_error_absolute:
                range_limits["ylim"][0] = min_error_absolute
            if range_limits["ylim"][1] < max_error_absolute:
                range_limits["ylim"][1] = max_error_absolute

            error_yaxis = [error_yaxis_negative, error_yaxis_positive]
            xaxis_point = [xaxis_data[0]]
            yaxis_point = [expected_yaxis[0]]
            error_yaxis_point = [[error_yaxis[0][0]], [error_yaxis[1][0]]]
            eb = ax.errorbar(
                xaxis_point,
                yaxis_point,
                yerr=error_yaxis_point,
                color=color,
                fmt="none",
                capsize=4.0,
                ls="-",
                alpha=0.7,
            )
            eb[-1][0].set_linestyle("dashed")


    xticklabels = sorted(list(set(xticklabels)))

    node_array = xticklabels
    reduced_node_array = [node_array[0]]
    last_position = 0
    for i in range(len(node_array)-1):
        if node_array[i+1]/reduced_node_array[-1] > 1.4:
            reduced_node_array.append(node_array[i])

    xticklabels = reduced_node_array
    ax.set_xticks(xticklabels)
    ax.set_xticklabels(xticklabels)
    ax.set_xlim(range_limits["xlim"])
    ax.set_ylim(range_limits["ylim"])

    plot.legend(bbox_to_anchor=(0.5, 0.3))

    plot.savefig(
        os.path.join(
            output_dir,
            "plot.pdf",
        ),
        bbox_inches="tight",
    )
    plot.savefig(
        os.path.join(
            output_dir,
            "plot.png",
        ),
        bbox_inches="tight",
    )
    return "plot.pdf"


def generate_plot_tex_file(experiment_array, output_dir):
    plotting_data = prepare_plotting_data(experiment_array)
    pdf_filename = generate_plot_pdf_file(plotting_data, output_dir)

    plotfilename = os.path.join(output_dir, "plot.tex")

    with open(plotfilename, "w") as plotfile:
        plotfile.write("% This file was generated by jureap.\n")
        plotfile.write("\\exacbplot{" + pdf_filename + "}{Caption}\n")


def generate_csv_table_tex_file(experiment_array, output_dir):
    tablefilename = os.path.join(output_dir, "table.tex")
    with open(tablefilename, "w") as tablefile:
        tablefile.write("% This file was generated by jureap.\n")

        for experiment in experiment_array:
            csv_file = os.path.join(
                "data", experiment.output_pipeline_dir(), experiment.prefix() + ".csv"
            )
            tablefile.write("\\exacbtable{" + csv_file + "}{Caption}\n")


def generate_json_tex_file(experiment_array, output_dir):
    jsonfilename = os.path.join(output_dir, "json.tex")
    with open(jsonfilename, "w") as jsonfile:
        jsonfile.write("% This file was generated by jureap.\n")

        for experiment in experiment_array:
            json_file = os.path.join(
                "data", experiment.output_pipeline_dir(), experiment.prefix() + ".json"
            )
            jsonfile.write("\\lstinputlisting[caption=Caption]{" + json_file + "}\n")


def generate_author_tex_file(output_dir):
    authorfilename = os.path.join(output_dir, "author.tex")
    with open(authorfilename, "w") as authorfile:
        authorfile.write("% This file was generated by jureap.\n")
        authorfile.write("\\title{Scaling Evaluation Report}\n")


def compile_report_pdf(output_dir):
    subprocess.run(["make", "debug"], cwd=output_dir, env=os.environ)


def prepare_report_dir(output_dir, share_dir):
    texdir = os.path.join(share_dir, "jureap/tex/jedi")
    shutil.copytree(texdir, output_dir)


def write_json_data(experiment_array, output_dir):
    json_dir = os.path.join(output_dir, "json")
    os.makedirs(json_dir, exist_ok=True)
    for experiment in experiment_array:
        json_filepath = os.path.join(
            json_dir, experiment.pipeline() + "." + experiment.prefix() + ".json"
        )
        with open(json_filepath, "w") as jsonfile:
            json.dump(experiment.json_repr(), jsonfile, indent=4)

def sort_csv_file(input_file, output_file):
    with open(input_file, "r") as input_csv:
        lines = input_csv.read().splitlines()[:-1]
        header = lines[0]
        node_index = header.split(",").index("nodes")
        data = [line.strip().split(",") for line in lines[1:]]
        data.sort(key=lambda x: int(x[node_index]))
        with open(output_file, "w") as output_csv:
            output_csv.write(header)
            for line in data:
                output_csv.write(",".join(line) + "\n")

def copy_raw_data(input_dir, experiment_array, output_dir):
    data_dir = os.path.join(output_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    for experiment in experiment_array:
        output_experiment_reldir = experiment.pipeline() + str(".") + experiment.prefix()
        output_experiment_dir = os.path.join(data_dir, output_experiment_reldir)
        input_experiment_dir = os.path.join(input_dir, experiment.pipeline_dir())
        csv_filepath = os.path.join(input_experiment_dir, experiment.prefix() + ".csv")
        json_filepath = os.path.join(input_experiment_dir, experiment.prefix() + ".json")
        os.makedirs(output_experiment_dir, exist_ok=True)
        output_csv_file = os.path.join(output_experiment_dir, experiment.prefix() + ".csv")
        sort_csv_file(csv_filepath, output_csv_file)
        shutil.copy(json_filepath, output_experiment_dir)


def generate(input_dir, experiment_array, output_dir, share_dir, tmp_dir):
    prepare_report_dir(output_dir, share_dir)
    copy_raw_data(input_dir, experiment_array, output_dir)
    generate_plot_tex_file(experiment_array, output_dir)
    generate_csv_table_tex_file(experiment_array, output_dir)
    generate_json_tex_file(experiment_array, output_dir)
    write_json_data(experiment_array, output_dir)
    generate_author_tex_file(output_dir)
    compile_report_pdf(output_dir)

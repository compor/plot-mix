#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter, ScalarFormatter, NullLocator


def log_10_product(x, pos):
    """Replace the default log-plot exponential labels with integer labels.
    The two args are the value and tick position.
    Label ticks with the product of the exponentiation"""
    return '%1i' % (x)


def unit_multiples(x, pos, multiple_base, multiple_exp, data):
    """Replace the default log-plot exponential labels with integer labels.
    The two args are the value and tick position.
    Label ticks with the product of the exponentiation"""
    return '%1i' % (data[pos] / pow(multiple_base, multiple_exp))


def create_plot(csvfile, pdf_out_file, config):
    df = pd.read_csv(csvfile,
                     sep=',',
                     comment='#',
                     skipinitialspace=True,
                     skip_blank_lines=True,
                     low_memory=True,
                     error_bad_lines=False,
                     warn_bad_lines=True)

    _, axis = plt.subplots(1, 1)

    colors = []

    if 'colors' in config:
        colors = config['colors']
    else:
        # fallback to grayscale values
        cmap = cm.get_cmap('Greys')
        step = 1.0 / len(df.columns)
        for i in range(0, len(df.columns)):
            colors.append(cmap((i + 1) * step))

    bar_edgecolor = 'black'
    if 'bar_edgecolor' in config:
        bar_edgecolor = config['bar_edgecolor']

    bar_linewidth = 1.0
    if 'bar_linewidth' in config:
        bar_linewidth = config['bar_linewidth']

    df.plot(kind='bar',
            ax=axis,
            x=config['xaxis'],
            y=config['yaxis'],
            use_index=True,
            logy=bool(config['yplotlog']),
            width=float(config['bar_width']),
            edgecolor=bar_edgecolor,
            linewidth=bar_linewidth,
            color=colors)
    if bool(config['yplotlog']):
        axis.set_yscale('symlog')

    plt.xticks(rotation=config['rotate_xticks'])

    if 'ylim' in config:
        axis.set_ylim(config['ylim'])
    if 'yticks' in config:
        plt.yticks(config['yticks'])

    # add a pattern to a bar
    # axis.patches[0].set_hatch(patterns[0])

    # formatter = FuncFormatter(log_10_product)
    # axis.yaxis.set_major_formatter(formatter)
    axis.yaxis.set_major_formatter(ScalarFormatter())
    axis.yaxis.set_minor_locator(NullLocator())

    if 'xaxis_multiple_base' in config:
        base = int(config['xaxis_multiple_base'])
        exp = 1
        if 'xaxis_multiple_exp' in config:
            exp = int(config['xaxis_multiple_exp'])

        def xformat(x, pos): return unit_multiples(
            x, pos, base, exp, list(df[config['xaxis']]))
        axis.xaxis.set_major_formatter(FuncFormatter(xformat))

    axis.set_xlabel(config['xlabel'])
    axis.set_ylabel(config['ylabel'])

    if bool(config['legend']):
        if 'legend_anchor' in config:
            axis.legend(bbox_to_anchor=config['legend_anchor'])
        if 'legend_linewidth' in config:
            axis.get_legend().get_frame().set_linewidth(
                float(config['legend_linewidth']))
    else:
        axis.get_legend().remove()

    if 'grid_axis' in config:
        axis.grid(axis=config['grid_axis'])

    plt.tight_layout(pad=0.2)

    pdf_fig = PdfPages(pdf_out_file)
    plt.savefig(pdf_fig, format='pdf')
    pdf_fig.close()


#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate speedup bar chart.')
    parser.add_argument('-f', '--file', required=True, type=str)
    parser.add_argument('-c', '--config', required=True, type=str)
    parser.add_argument('-d',
                        '--dest-dir',
                        required=False,
                        type=str,
                        default='.')
    prog_args = parser.parse_args()

    if not os.path.exists(prog_args.file):
        print("File {} does not exist".format(prog_args.file), file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(prog_args.config):
        print("File {} does not exist".format(prog_args.file), file=sys.stderr)
        sys.exit(1)

    if os.path.exists(prog_args.dest_dir) and os.path.isfile(
            prog_args.dest_dir):
        print("File {} already exists".format(prog_args.file), file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(prog_args.dest_dir):
        os.mkdir(prog_args.dest_dir)

    with open(prog_args.config, 'r') as config_file:
        plot_config = json.load(config_file)

    filename, _ = os.path.splitext(prog_args.file)
    if prog_args.dest_dir != '.':
        filename = os.path.basename(filename)

    pdf_out_file = prog_args.dest_dir + '/' + filename + '.pdf'

    create_plot(prog_args.file, pdf_out_file, plot_config)

    sys.exit(0)

#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
import argparse
import json
import pandas as pd
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def create_plot(csvfile, config):
    df = pd.read_csv(csvfile, sep=',', low_memory=True, error_bad_lines=False)
    filename, _ = os.path.splitext(csvfile)

    group = list(df['Version'].unique())

    data = []
    for i in group:
        data.append(df[df['Version'] == i])

    color = []
    for i in range(len(df['Version'].unique())):
        color.append('#2366C2')

    # Create plot
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.xaxis.grid(which='major', color='gray', linestyle='--', alpha=0.5)
    axis.yaxis.grid(which='major', color='gray', linestyle='--', alpha=0.5)

    # custom offsets
    offsets = []
    for i in group:
        offsets.append((0, 0))

    # custom offset exceptions
    # offsets[0] = (100, 20)
    # offsets[2] = (-20, -30)
    # offsets[3] = (110, 20)
    # offsets[4] = (100, 15)
    # offsets[5] = (-20, 10)

    i = 0
    for d, c, g in zip(data, color, group):
        x = d['Measured']
        y = d['Expected']
        s = 1500
        axis.scatter(x, y, alpha=0.4, c=c, edgecolors='k', s=s, label=g)

        txt = list(d['Version'])[0]
        txt_color = 'black'
        axis.annotate(txt, (list(x)[0], list(y)[0]),
                      fontsize=18,
                      color=txt_color,
                      xytext=offsets[i],
                      textcoords='offset points',
                      horizontalalignment='center',
                      verticalalignment='center')
        i = i + 1

    axis.set_xlim(0, 12)
    axis.set_ylim(0, 12)

    axis.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xlabel("Measured Rank")
    plt.ylabel("Estimated Rank")
    plt.tight_layout(pad=0.4)

    pdf_fig = PdfPages(filename + '.pdf')
    plt.savefig(pdf_fig, format='pdf')
    pdf_fig.close()


#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate speedup bar chart.')
    parser.add_argument('-f', '--file', required=True, type=str)
    # parser.add_argument('-c', '--config', required=True, type=str)
    parser.add_argument('-d',
                        '--dest-dir',
                        required=False,
                        type=str,
                        default='.')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("File {} does not exist".format(args.file), file=sys.stderr)
        sys.exit(1)

    # if not os.path.exists(args.config):
    # print("File {} does not exist".format(args.file), file=sys.stderr)
    # sys.exit(1)

    # with open(args.config, 'r') as config_file:
    # plot_config = json.load(config_file)
    plot_config = json.loads('{}')

    create_plot(args.file, plot_config)

    sys.exit(0)

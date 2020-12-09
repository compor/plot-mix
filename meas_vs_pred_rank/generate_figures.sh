#!/usr/bin/env bash

chmod a+x ./graph.py

./graph.py -f data.csv

cp data.pdf ../../figures/prog_opt/rank_corr_plot_prog_opt.pdf

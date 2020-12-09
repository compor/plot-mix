#!/usr/bin/env bash

mkdir -p out

./graph.py \
  -c ./config.json \
  -f ./data.csv \
  -d out

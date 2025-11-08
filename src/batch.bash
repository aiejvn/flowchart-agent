#!/bin/bash
# bash ../activate/Scripts/activate;
# python benchmarking.py -m gpt-4o-mini -i data/cd.jsonl -f flowcharts/rag.json -o 'data/results' -k 10
source ../.venv/Scripts/activate
python benchmarking.py -m gpt-4o-mini -i data/cd2.jsonl -f flowcharts/updated_rag.json -o 'data/results' -k 2
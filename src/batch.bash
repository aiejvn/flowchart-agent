#!/bin/bash
bash ../activate/Scripts/activate;
python benchmarking.py -m gpt-4o-mini -i data/cd.jsonl -f flowcharts/rag.json -o 'data/results' -k 10
from flowchart import load_flowchart, init
import json
import dotenv

import argparse

from tqdm import *


def example_test(input_file, flowchart_file, model, n=-1):
    fc = load_flowchart(flowchart_file)
    init(model)

    if input_file.endswith('jsonl'):
        with open(input_file, 'r') as f:
            data = [json.loads(x) for x in f.readlines()] # this example assumes the input is already in jsonl format

    res = []
    if n == -1:
        n = len(data)

    # print(data[0])
    for d in tqdm(data[:n]):
        result = fc.execute(d)
        # print(result[-1])
        # result[0]['gold_label'] = d['gold_label'][0]
        res.append({'result': result[0].__dict__(), 'gold_label': d['gold_label'][0]})

    return res

if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help = "model name", default='gpt-4o-mini')
    parser.add_argument("-i", "--input", help = "input file name")
    parser.add_argument("-f", "--flow", help = "flowchart")
    parser.add_argument("-k", "--topk", help = "top k", type=int)
    parser.add_argument("-o", "--out", help = "output folder")

    args = parser.parse_args()

    models = ['gpt-4o', 'o3', 'o3-deep-research']
    for m in models:
        
        res = example_test(args.input, args.flow, m, args.topk)

        with open(f"{args.out}/{args.input.split('/')[-1].split('.')[0]}_{m}_{args.flow.split('/')[-1].split('.')[0]}.json", 'w') as f:
            f.write(json.dumps(res, indent=4))
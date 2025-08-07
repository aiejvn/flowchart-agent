from flowchart import load_flowchart, init
import json
import dotenv


def example_test(input_file, flowchart_file, n=-1):
    fc = load_flowchart(flowchart_file)
    init('gpt-4o-mini', 'openai')

    if input_file.endswith('jsonl'):
        with open(input_file, 'r') as f:
            data = [json.loads(x) for x in f.readlines()] # this example assumes the input is already in jsonl format

    res = []
    if n == -1:
        n = len(data)

    for d in data[:n]:
        result = fc.execute(d)
        # print(result[-1])

        res.append(result)

    return res

dotenv.load_dotenv()
res = example_test('src/data/cd.jsonl', 'src/flowcharts/self_reflection.json', n=10)

with open('src/data/cd.txt', 'w') as f:
    f.write(json.dumps([[y.__dict__() for y in x] for x in res], indent=4))
from flowchart import load_flowchart
from utils import FlowchartTask_llm_execution, init
import json
import dotenv


def example_test(input_file, flowchart_file):
    fc = load_flowchart(flowchart_file)
    init('gpt-4o-mini', 'openai')

    if input_file.endswith('jsonl'):
        with open(input_file, 'r') as f:
            data = [json.loads(x) for x in f.readlines()] # this example assumes the input is already in jsonl format

    res = []

    for d in data:
        result = fc.execute(FlowchartTask_llm_execution, d['query'])
        print(result[-1])

        res.append(result)

    return res

dotenv.load_dotenv()
example_test('src/data/sample.jsonl', 'src/flowcharts/self_reflection.json')
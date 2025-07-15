from typing import List, Callable, Any, Tuple, Dict
import json


class FlowchartTask:
    def __init__(self, inp):
        self.type = inp['type']
        if self.type == 'api':
            if 'url' not in inp or 'endpoint' not in inp:
                pass
            else:                
                self.url = inp['url']
                self.endpoint = inp['endpoint']
                self.outputSelection = inp['output_strat'] # one of these options: concat, first, random
        elif self.type == 'llm':
            self.instructions = inp['instructions']
            self.inputFormat = (inp['input_format'] if 'input_format' in inp else None)
            self.outputFormat = (inp['output_format'] if 'input_format' in inp else None)

    def __repr__(self):
        return f"FlowchartNode(name={self.name.__repr__()}, instructions={self.instructions.__repr__()}, inputFormat={self.inputFormat.__repr__()}, outputFormat={self.outputFormat.__repr__()})"

    def to_prompt(self, input, input_reg = '[input]'):
        """
        Convert a FlowchartTask to a prompt string.
        """
        assert self.type == 'llm', 'node type mismatch, must be an llm call'

        inp_form = f'Input Format: {self.inputFormat}'
        out_form = f'Output Format: {self.outputFormat}'
        instructions = self.instructions.replace(input_reg, input)

        return f"""{instructions}
    {(inp_form if self.inputFormat else '')}
    {(out_form if self.outputFormat else '')}
    """


class FlowchartTaskResult:
    def __init__(self, value: Any, executionDetails: Dict):
        self.value = value
        self.executionDetails = executionDetails

    def __repr__(self):
        return f"FlowchartNodeOutput(value={self.value.__repr__()}, executionDetails={self.executionDetails.__repr__()})"


# This is a linear flowchart structure, the nodes are connected in a sequence.
class Flowchart:
    # nodes: List[FlowchartTask]

    def __init__(self, nodes: List[FlowchartTask]):
        self.nodes = nodes

    def execute(self, function: Callable[[FlowchartTask, FlowchartTaskResult], Any], input: Any) -> List[FlowchartTaskResult]:
        """
        Execute a Flowchart and return the output.
        This function .
        """
        assert isinstance(
            self.nodes, list), "flowchart must be a list of FlowchartTask instances"

        results = [FlowchartTaskResult(value=input, executionDetails={
                                    "initial_input": input})]
        for node in self.nodes:
            results.append(function(node, results[-1].value))

        return results  # return all outputs, including the initial input as the first element



def load_flowchart(filename: str):
    with open(filename, 'r') as f:
        data = json.load(f)

    return Flowchart([FlowchartTask(x) for x in data])
from typing import List, Callable, Any, Tuple, Dict
import json

import random

from globals import REQUESTS_MAPPING, OUTPUT_FORMAT_MAPPING

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


llm = None

def init(model_name, provider, t=0.3 ):
    global llm
    llm = init_chat_model(
            model_name,
            model_provider=provider,
            temperature=t)



class FlowchartTask:
    def __init__(self, inp):
        self.type = inp['type']
        if self.type == 'api':
            if 'url' not in inp or 'endpoint' not in inp:
                pass
            else:                
                self.url = inp['url']
                self.endpoint = inp['endpoint']
                self.outputSelection = inp['output_strat'] # one of these options: concat, topk, random
        elif self.type == 'llm':
            self.instructions = inp['instructions']
            self.inputFormat = (inp['input_format'] if 'input_format' in inp else None)
            self.outputFormat = (inp['output_format'] if 'output_format' in inp else None)

    def __repr__(self):
        return f"FlowchartNode(name={self.name.__repr__()}, instructions={self.instructions.__repr__()}, inputFormat={self.inputFormat.__repr__()}, outputFormat={self.outputFormat.__repr__()})"

    def to_prompt(self, input, docs, input_reg = '[input]', doc_reg='[docs]'):
        """
        Convert a FlowchartTask to a prompt string.
        """
        assert self.type == 'llm', 'node type mismatch, must be an llm call'

        inp_form = f'Input Format: {self.inputFormat}'
        out_form = f'Output Format: {self.outputFormat}'
        instructions = self.instructions.replace(input_reg, input)
        if len(docs) > 0:
            instructions = instructions.replace(doc_reg, '\n'.join(['{0}: {1}'.format(x['name'], x['content']) for x in docs]))
        else:
            instructions = instructions.replace(doc_reg, '')

        return f"""{instructions}
    {(inp_form if self.inputFormat is not None else '')}
    {(out_form if self.outputFormat is not None else '')}
    """

class FlowchartTaskResult:
    def __init__(self, value: Any, executionDetails: Dict):
        self.value = value
        self.executionDetails = executionDetails

    def __dict__(self):
        return {'value': self.value, 'executionDetails': ([x.content for x in self.executionDetails['promptMessages']] if 'promptMessages' in self.executionDetails else self.executionDetails)}
    def __repr__(self):
        return f"FlowchartNodeOutput(value={self.value.__repr__()}, executionDetails={self.executionDetails.__repr__()})"


# This is a linear flowchart structure, the nodes are connected in a sequence.
class Flowchart:
    # nodes: List[FlowchartTask]

    def __init__(self, nodes: List[FlowchartTask]):
        self.nodes = nodes


    def llm_execution(self, node: FlowchartTask, input: str) -> FlowchartTaskResult:
        """
        Execute a FlowchartNode and return the output.
        This function simulates the execution of a flowchart node using a basic LLM call.

        currently, the audit is just the prompt and the response from the LLM.
        """
        assert isinstance(
                node, FlowchartTask), "node must be a FlowchartTask instance"
        if type(input) == str:
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=node.to_prompt(input, [])),
            ]
        else:
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=node.to_prompt(input['query'], input['supporting_docs'])),
            ]
        response = llm.invoke(messages)
        return FlowchartTaskResult(value=response.content, executionDetails={"promptMessages": messages, "response": response})


    def api_execution(self, node: FlowchartTask, input, headers={}) -> FlowchartTaskResult:
        if node.url in REQUESTS_MAPPING:
            response = REQUESTS_MAPPING[node.url](url=''.join(['http://', node.url, node.endpoint]), data=input, headers=headers)
        else:
            return "Not supported"
        
        res = response.json()
        text = []
        if node.outputSelection == 'concat':
            text = res
        elif node.outputSelection.startswith('top'): # top k, where k is < 10
            text.extend(res[:int(node.outputSelection[-1])])
        elif node.outputSelection == 'random': # random k, where k is < 10
            text.append(random.sample(res, k=int(node.outputSelection[-1])))

        out = OUTPUT_FORMAT_MAPPING[node.url](text)
        
        return FlowchartTaskResult(value='\n**********\n'.join(out), executionDetails={'full_response': res, 'input': input})


    def execute(self, input: Any) -> List[FlowchartTaskResult]:
        """
        Execute a Flowchart and return the output.
        This function .
        """
        assert isinstance(
            self.nodes, list), "flowchart must be a list of FlowchartTask instances"

        results = [FlowchartTaskResult(value=input, executionDetails={
                                    "initial_input": input})]
        for node in self.nodes:
            if node.type == 'llm':
                results.append(self.llm_execution(node,results[-1].value))
            elif node.type == 'api':
                data = {'query': results[-1].value, 'collection': 'constructive_dismissal'}
                results.append(self.api_execution(node, data))

        return results[1:]  # return all outputs, except for the initial input as the first element


def load_flowchart(filename: str):
    with open(filename, 'r') as f:
        data = json.load(f)

    return Flowchart([FlowchartTask(x) for x in data])
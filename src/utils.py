import json
from flowchart import Flowchart, FlowchartTask, FlowchartTaskResult

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def google_form(results):
    return [f"Title: {x['title']}\n\nSnippet: {x['snippet']}" for x in results]

OUTPUT_FORMAT_MAPPING = {
    'google.com': google_form, 
}

EVAL_METRICS = {
    'example.json': ['bleu']
}

llm = None

def init(model_name, provider, t=0.3 ):
    global llm
    llm = init_chat_model(
            model_name,
            model_provider=provider,
            temperature=t)

def FlowchartTask_llm_execution(node: FlowchartTask, input: str) -> FlowchartTaskResult:
    """
    Execute a FlowchartNode and return the output.
    This function simulates the execution of a flowchart node using a basic LLM call.

    currently, the audit is just the prompt and the response from the LLM.
    """
    assert isinstance(
        node, FlowchartTask), "node must be a FlowchartTask instance"
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=node.to_prompt(input)),
    ]
    response = llm.invoke(messages)
    return FlowchartTaskResult(value=response.content, executionDetails={"promptMessages": messages, "response": response})
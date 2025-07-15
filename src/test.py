
from flowchart import FlowchartTask, execute_Flowchart
from utils import FlowchartTask_llm_execution

import random
import string
import json


def generate_random_string(length: int) -> str:
    """Generate a string of specified length using letters, digits, and punctuation using python 'random'."""
    assert length >= 0, "Length must be a nonnegative integer"
    characters = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(characters) for _ in range(length))


def test_FlowchartTask_llm_execution():
    task = FlowchartTask(
        name="Test Task",
        instructions="This is a test node for the flowchart. For this test, just return the input as output and do not change it.",
        inputFormat="some string input",
        outputFormat="the same format as the input"
    )

    print("Testing FlowchartTask_llm_execution:")
    input = generate_random_string(10)
    results = FlowchartTask_llm_execution(task, input)
    testLog = {
        "node": task,
        "input": input,
        "result": results
    }
    print("```json")
    print(json.dumps(testLog, default=lambda o: o.__dict__, indent=2))
    print("```")


def test_execute_Flowchart():
    """Test the execute_Flowchart function."""
    task1 = FlowchartTask(
        name="Task 1",
        instructions="convert the input to a single number in base 10.",
        inputFormat="a number in english wording such as 'forty two'",
        outputFormat="just a single decimal number"
    )
    task2 = FlowchartTask(
        name="Task 2",
        instructions="convert the base 10 number to an english worded representation such as 'ten thousand' or 'fifty five'.",
        inputFormat="a number is base 10",
        outputFormat="number in english wording"
    )

    print("Testing execute_Flowchart:")
    flowchart = [task1, task2]
    input = "two hundred and fifty six"
    result = execute_Flowchart(flowchart, FlowchartTask_llm_execution, input)
    testLog = {
        "flowchart": flowchart,
        "input": input,
        "result": result
    }
    print("```json")
    print(json.dumps(testLog, default=lambda o: o.__dict__, indent=2))
    print("```")


def main():
    """Run all tests."""
    test_FlowchartTask_llm_execution()
    test_execute_Flowchart()
    print("-----------------")
    print("All tests passed!")


if __name__ == "__main__":
    main()

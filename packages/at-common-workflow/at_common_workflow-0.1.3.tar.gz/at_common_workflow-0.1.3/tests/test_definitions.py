import pytest
from src.definitions import (
    TaskParameter,
    TaskDefinition,
    WorkflowDefinition,
    WorkflowBuilder,
    TaskLoader
)
from src.core.context import Context
from src.core.workflow import Workflow

# TaskParameter Tests
def test_task_parameter_default_values():
    param = TaskParameter(type="str")
    assert param.type == "str"
    assert param.default is None
    assert param.required is True

def test_task_parameter_custom_values():
    param = TaskParameter(type="int", default=42, required=False)
    assert param.type == "int"
    assert param.default == 42
    assert param.required is False

def test_task_parameter_complex_type():
    param = TaskParameter(type="List[str]", default=["a", "b"], required=True)
    assert param.type == "List[str]"
    assert param.default == ["a", "b"]
    assert param.required is True

# TaskDefinition Tests
def test_task_definition_minimal():
    task_def = TaskDefinition(
        name="minimal_task",
        module="test_module",
        function="test_function"
    )
    assert task_def.name == "minimal_task"
    assert task_def.parameters == None
    assert task_def.requires == []
    assert task_def.provides == []

def test_task_definition_full():
    task_def = TaskDefinition(
        name="full_task",
        module="test_module",
        function="test_function",
        parameters={"param1": 42, "param2": "test"},
        requires=["input1", "input2"],
        provides=["output1", "output2"]
    )
    assert task_def.name == "full_task"
    assert task_def.parameters == {"param1": 42, "param2": "test"}
    assert task_def.requires == ["input1", "input2"]
    assert task_def.provides == ["output1", "output2"]

# WorkflowDefinition Tests
def test_workflow_definition_minimal():
    task_def = TaskDefinition(
        name="test_task",
        module="test_module",
        function="test_function"
    )
    workflow_def = WorkflowDefinition(
        name="minimal_workflow",
        tasks=[task_def]
    )
    assert workflow_def.name == "minimal_workflow"
    assert len(workflow_def.tasks) == 1
    assert workflow_def.initial_context is None

def test_workflow_definition_multiple_tasks():
    tasks = [
        TaskDefinition(name=f"task_{i}", module="test_module", function="test_function")
        for i in range(3)
    ]
    workflow_def = WorkflowDefinition(
        name="multi_task_workflow",
        tasks=tasks,
        initial_context={"key": "value"}
    )
    assert len(workflow_def.tasks) == 3
    assert workflow_def.initial_context == {"key": "value"}

# TaskLoader Tests
async def test_task_loader_with_optional_parameters():
    async def test_func(context, required_param: str, optional_param: int = 10):
        context.set("result", f"{required_param}_{optional_param}")
    
    task = TaskLoader.create_wrapped_task(
        func=test_func,
        parameters={"required_param": "test"},
        requires=[],
        provides=["result"]
    )
    
    context = Context()
    await task.execute(context)
    assert context.get("result") == "test_10"

async def test_task_loader_missing_required_parameter():
    async def test_func(context, required_param: str):
        context.set("result", required_param)
    
    task = TaskLoader.create_wrapped_task(
        func=test_func,
        parameters={},
        requires=[],
        provides=["result"]
    )
    
    context = Context()
    with pytest.raises(ValueError, match="Required parameter.*not provided"):
        await task.execute(context)

def test_task_loader_invalid_module_path():
    with pytest.raises(ImportError):
        TaskLoader.load_function("invalid.module.path", "function")

# WorkflowBuilder Tests
async def test_workflow_builder_empty_workflow():
    workflow_json = {
        "name": "empty_workflow",
        "tasks": []
    }
    
    context = Context()
    workflow = WorkflowBuilder.from_json(workflow_json, context)
    assert isinstance(workflow, Workflow)
    assert len(workflow.tasks) == 0

async def test_workflow_builder_complex_dependencies():
    # Define test tasks
    async def task_a(context, value: int):
        context.set("a_output", value * 2)
    
    async def task_b(context, multiplier: int):
        a_value = context.get("a_output")
        context.set("b_output", a_value * multiplier)
    
    async def task_c(context):
        b_value = context.get("b_output")
        context.set("final_output", b_value + 10)
    
    globals().update({
        "task_a": task_a,
        "task_b": task_b,
        "task_c": task_c
    })
    
    workflow_json = {
        "name": "complex_workflow",
        "tasks": [
            {
                "name": "task_a",
                "module": __name__,
                "function": "task_a",
                "parameters": {"value": 5},
                "provides": ["a_output"]
            },
            {
                "name": "task_b",
                "module": __name__,
                "function": "task_b",
                "parameters": {"multiplier": 3},
                "requires": ["a_output"],
                "provides": ["b_output"]
            },
            {
                "name": "task_c",
                "module": __name__,
                "function": "task_c",
                "requires": ["b_output"],
                "provides": ["final_output"]
            }
        ],
        "initial_context": {"start": "value"}
    }
    
    context = Context()
    workflow = WorkflowBuilder.from_json(workflow_json, context)
    
    async for _ in workflow.execute():
        pass
    
    assert context.get("final_output") == 40  # (5 * 2 * 3) + 10

def test_workflow_builder_invalid_task_definition():
    workflow_json = {
        "name": "invalid_workflow",
        "tasks": [{
            "name": "invalid_task",
            # Missing required fields module and function
            "parameters": {}
        }]
    }
    
    context = Context()
    with pytest.raises(Exception):
        WorkflowBuilder.from_json(workflow_json, context)

@pytest.mark.parametrize("invalid_field", [
    {"name": None},
    {"module": ""},
    {"function": ""},
    {"parameters": "not_a_dict"},
    {"requires": "not_a_list"},
    {"provides": "not_a_list"}
])
def test_workflow_builder_invalid_field_types(invalid_field):
    base_task = {
        "name": "test_task",
        "module": "test_module",
        "function": "test_function",
        "parameters": {},
        "requires": [],
        "provides": []
    }
    
    invalid_task = {**base_task, **invalid_field}
    workflow_json = {
        "name": "invalid_workflow",
        "tasks": [invalid_task]
    }
    
    context = Context()
    with pytest.raises(Exception):
        WorkflowBuilder.from_json(workflow_json, context)

import pytest
import asyncio
from src import Workflow, TaskStatus, Context, DependencyNotFoundError, CircularDependencyError
from src.core.context import Context
from src.models.progress import TaskProgress, TaskProgressStatus

# Basic Functionality Tests
async def test_basic_workflow_execution():
    context = Context()
    workflow = Workflow("test_basic", context)

    @workflow.task()
    async def simple_task(context):
        context.set("result", "done")
    
    progress_events = []
    async for progress in workflow.execute():
        progress_events.append(progress)
    
    assert context.get("result") == "done"
    assert workflow.tasks["simple_task"].status == TaskStatus.COMPLETED
    assert len(progress_events) == 2
    assert progress_events[0] == TaskProgress("simple_task", TaskProgressStatus.STARTED)
    assert progress_events[1] == TaskProgress("simple_task", TaskProgressStatus.COMPLETED)

# Dependency Tests
async def test_workflow_dependencies():
    context = Context()
    workflow = Workflow("test_deps", context)
    
    @workflow.task(provides=["data1"])
    async def task1(context):
        context.set("data1", "value1")
    
    @workflow.task(requires=["data1"], provides=["data2"])
    async def task2(context):
        data = context.get("data1")
        context.set("data2", f"{data}_processed")
    
    @workflow.task(requires=["data2"])
    async def task3(context):
        data = context.get("data2")
        context.set("final", f"{data}_final")
    
    async for _ in workflow.execute():
        pass
    
    assert context.get("final") == "value1_processed_final"

# Parallel Execution Tests
async def test_parallel_execution():
    context = Context()
    workflow = Workflow("test_parallel", context)
    execution_order = []
    progress_events = []
    
    @workflow.task()
    async def slow_task(context):
        await asyncio.sleep(0.2)
        execution_order.append("slow")
    
    @workflow.task()
    async def fast_task(context):
        await asyncio.sleep(0.1)
        execution_order.append("fast")
    
    async for progress in workflow.execute():
        progress_events.append(progress)
    
    assert execution_order == ["fast", "slow"]
    assert len(progress_events) == 4  # 2 tasks * 2 events (STARTED, COMPLETED)
    assert all(isinstance(p, TaskProgress) for p in progress_events)

# Error Handling Tests
async def test_task_failure_propagation():
    context = Context()
    workflow = Workflow("test_error", context)
    progress_events = []
    
    @workflow.task()
    async def failing_task(context):
        raise ValueError("Expected failure")
    
    with pytest.raises(ValueError, match="Expected failure"):
        async for progress in workflow.execute():
            progress_events.append(progress)
    
    assert workflow.tasks["failing_task"].status == TaskStatus.FAILED
    assert len(progress_events) == 2
    assert progress_events[0] == TaskProgress("failing_task", TaskProgressStatus.STARTED)
    assert progress_events[1] == TaskProgress("failing_task", TaskProgressStatus.FAILED)

async def test_invalid_dependency():
    context = Context()
    workflow = Workflow("test_invalid_dep", context)
    
    @workflow.task(requires=["nonexistent"])
    async def dependent_task(context):
        pass
    
    with pytest.raises(DependencyNotFoundError):
        async for _ in workflow.execute():
            pass

# Circular Dependency Tests
async def test_circular_dependency_detection():
    context = Context()
    workflow = Workflow("test_circular", context)
    
    @workflow.task(requires=["b"], provides=["a"])
    async def task_a(context):
        pass
    
    @workflow.task(requires=["a"], provides=["b"])
    async def task_b(context):
        pass
    
    with pytest.raises(CircularDependencyError, match="Circular dependency detected"):
        async for _ in workflow.execute():
            pass

# Context Access Tests
async def test_context_access_patterns():
    context = Context()
    workflow = Workflow("test_context_access", context)
    
    @workflow.task(provides=["key1"])
    async def writer_task(context):
        context.set("key1", "value1")
    
    @workflow.task(requires=["key1"])
    async def reader_task(context):
        assert context.get("key1") == "value1"
        assert "key1" in context
        context.delete("key1")
        assert "key1" not in context
    
    async for _ in workflow.execute():
        pass

# Non-async Function Test
async def test_non_async_function():
    context = Context()
    workflow = Workflow("test_non_async", context)
    
    @workflow.task()
    def sync_task(context):  # Not async
        pass
    
    with pytest.raises(ValueError, match="must be an async function"):
        async for _ in workflow.execute():
            pass

# Multiple Tasks with Same Provides
async def test_duplicate_provides():
    context = Context()
    workflow = Workflow("test_duplicate", context)
    
    @workflow.task(provides=["data"])
    async def task1(context):
        context.set("data", "done")
    
    # Test that adding a duplicate provider raises ValueError
    with pytest.raises(ValueError, match="Multiple tasks provide the same data"):
        @workflow.task(provides=["data"])
        async def task2(context):
            pass
    
    async for _ in workflow.execute():
        pass
    
    assert context.get("data") == "done"

# Empty Workflow Test
async def test_empty_workflow():
    context = Context()
    workflow = Workflow("test_empty", context)
    async for _ in workflow.execute():
        pass
    assert isinstance(context, Context)

# Complex Dependency Chain
async def test_complex_dependency_chain():
    context = Context()
    workflow = Workflow("test_complex", context)
    execution_order = []
    
    @workflow.task(provides=["a"])
    async def task_a(context):
        execution_order.append("a")
        context.set("a", "a")
    
    @workflow.task(requires=["a"], provides=["b"])
    async def task_b(context):
        execution_order.append("b")
        context.set("b", context.get("a") + "b")
    
    @workflow.task(requires=["b"], provides=["c"])
    async def task_c(context):
        execution_order.append("c")
        context.set("c", context.get("b") + "c")
    
    @workflow.task(requires=["a", "c"])
    async def task_d(context):
        execution_order.append("d")
        context.set("result", context.get("a") + context.get("c"))
    
    async for _ in workflow.execute():
        pass
    
    assert execution_order == ["a", "b", "c", "d"]
    assert context.get("result") == "aabc"

# Cleanup Test
async def test_context_cleanup():
    context = Context()
    workflow = Workflow("test_cleanup", context)
    
    @workflow.task(provides=["temp"])
    async def task1(context):
        context.set("temp", "temporary")
    
    @workflow.task(requires=["temp"])
    async def task2(context):
        assert context.get("temp") == "temporary"
        context.clear()
    
    async for _ in workflow.execute():
        pass
    
    assert len(context._data) == 0

# Task Timeout Test
async def test_task_timeout():
    context = Context()
    workflow = Workflow("test_timeout", context)
    
    @workflow.task()
    async def long_running_task(context):
        await asyncio.sleep(10)  # Simulate long task
    
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.1):
            async for _ in workflow.execute():
                pass

# Task Cancellation Test
async def test_task_cancellation():
    context = Context()
    workflow = Workflow("test_cancel", context)
    was_cancelled = False
    
    @workflow.task()
    async def cancellable_task(context):
        nonlocal was_cancelled
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            was_cancelled = True
            raise

    # Create a wrapper coroutine to consume the async generator
    async def execute_workflow():
        async for _ in workflow.execute():
            pass

    task = asyncio.create_task(execute_workflow())
    await asyncio.sleep(0.1)
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task
    
    assert was_cancelled

async def test_preexisting_context_data():
    context = Context()
    # Set data before workflow creation
    context.set("pre_existing", "initial_value")
    workflow = Workflow("test_preexisting", context)
    
    @workflow.task(requires=["pre_existing"], provides=["modified"])
    async def modify_existing(context):
        pre_value = context.get("pre_existing")
        context.set("modified", f"{pre_value}_modified")
    
    @workflow.task(requires=["modified"])
    async def verify_data(context):
        assert context.get("modified") == "initial_value_modified"
        assert context.get("pre_existing") == "initial_value"
    
    async for _ in workflow.execute():
        pass
        
    assert context.get("pre_existing") == "initial_value"
    assert context.get("modified") == "initial_value_modified"

async def test_task_with_parameters():
    context = Context()
    workflow = Workflow("test_parameters", context)
    
    @workflow.task(parameters={"multiplier": 2})
    async def parameterized_task(context, multiplier: int):
        context.set("result", 10 * multiplier)
    
    async for _ in workflow.execute():
        pass
    
    assert context.get("result") == 20

async def test_multiple_parameters():
    context = Context()
    workflow = Workflow("test_multi_params", context)
    
    @workflow.task(
        parameters={
            "prefix": "test_",
            "suffix": "_done",
            "count": 3
        }
    )
    async def complex_params_task(context, prefix: str, suffix: str, count: int):
        result = f"{prefix}" + "x" * count + f"{suffix}"
        context.set("result", result)
    
    async for _ in workflow.execute():
        pass
    
    assert context.get("result") == "test_xxx_done"

async def test_parameters_with_dependencies():
    context = Context()
    workflow = Workflow("test_params_deps", context)
    
    @workflow.task(
        provides=["initial"],
        parameters={"value": 5}
    )
    async def provider_task(context, value: int):
        context.set("initial", value)
    
    @workflow.task(
        requires=["initial"],
        provides=["processed"],
        parameters={"multiplier": 2}
    )
    async def processor_task(context, multiplier: int):
        initial = context.get("initial")
        context.set("processed", initial * multiplier)
    
    async for _ in workflow.execute():
        pass
    
    assert context.get("initial") == 5
    assert context.get("processed") == 10

async def test_missing_parameter():
    context = Context()
    workflow = Workflow("test_missing_param", context)
    
    @workflow.task(parameters={})
    async def task_with_required_param(context, required_param: str):
        context.set("result", required_param)
    
    with pytest.raises(ValueError, match="Required parameter .* not provided"):
        async for _ in workflow.execute():
            pass

async def test_parameter_type_handling():
    context = Context()
    workflow = Workflow("test_param_types", context)
    
    @workflow.task(
        parameters={
            "int_param": 42,
            "str_param": "hello",
            "list_param": [1, 2, 3],
            "dict_param": {"key": "value"}
        }
    )
    async def type_check_task(
        context,
        int_param: int,
        str_param: str,
        list_param: list,
        dict_param: dict
    ):
        context.set("results", {
            "int": int_param,
            "str": str_param,
            "list": list_param,
            "dict": dict_param
        })
    
    async for _ in workflow.execute():
        pass
    
    results = context.get("results")
    assert isinstance(results["int"], int)
    assert isinstance(results["str"], str)
    assert isinstance(results["list"], list)
    assert isinstance(results["dict"], dict)
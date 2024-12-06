import pytest
import asyncio
from src import Workflow, TaskStatus, Context, DependencyNotFoundError, CircularDependencyError

# Basic Functionality Tests
async def test_basic_workflow_execution(workflow):
    @workflow.task()
    async def simple_task(context):
        context.set("result", "done")
    
    context = await workflow.execute()
    assert context.get("result") == "done"
    assert workflow.tasks["simple_task"].status == TaskStatus.COMPLETED

# Dependency Tests
async def test_workflow_dependencies():
    workflow = Workflow("test_deps")
    
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
    
    context = await workflow.execute()
    assert context.get("final") == "value1_processed_final"

# Parallel Execution Tests
async def test_parallel_execution():
    workflow = Workflow("test_parallel")
    execution_order = []
    
    @workflow.task()
    async def slow_task(context):
        await asyncio.sleep(0.2)
        execution_order.append("slow")
    
    @workflow.task()
    async def fast_task(context):
        await asyncio.sleep(0.1)
        execution_order.append("fast")
    
    await workflow.execute()
    assert execution_order == ["fast", "slow"]

# Error Handling Tests
async def test_task_failure_propagation():
    workflow = Workflow("test_error")
    
    @workflow.task()
    async def failing_task(context):
        raise ValueError("Expected failure")
    
    with pytest.raises(ValueError, match="Expected failure"):
        await workflow.execute()
    assert workflow.tasks["failing_task"].status == TaskStatus.FAILED

async def test_invalid_dependency():
    workflow = Workflow("test_invalid_dep")
    
    @workflow.task(requires=["nonexistent"])
    async def dependent_task(context):
        pass
    
    with pytest.raises(DependencyNotFoundError):
        await workflow.execute()

# Circular Dependency Tests
async def test_circular_dependency_detection():
    workflow = Workflow("test_circular")
    
    @workflow.task(requires=["b"], provides=["a"])
    async def task_a(context):
        pass
    
    @workflow.task(requires=["a"], provides=["b"])
    async def task_b(context):
        pass
    
    with pytest.raises(CircularDependencyError, match="Circular dependency detected"):
        await workflow.execute()

# Context Access Tests
async def test_context_access_patterns(workflow):
    @workflow.task(provides=["key1"])
    async def writer_task(context):
        context.set("key1", "value1")
    
    @workflow.task(requires=["key1"])
    async def reader_task(context):
        assert context.get("key1") == "value1"
        assert "key1" in context
        context.delete("key1")
        assert "key1" not in context
    
    await workflow.execute()

# Non-async Function Test
def test_non_async_function():
    workflow = Workflow("test_non_async")
    
    @workflow.task()
    def sync_task(context):  # Not async
        pass
    
    with pytest.raises(ValueError, match="must be an async function"):
        asyncio.run(workflow.execute())

# Multiple Tasks with Same Provides
async def test_duplicate_provides():
    workflow = Workflow("test_duplicate")
    
    @workflow.task(provides=["data"])
    async def task1(context):
        context.set("data", "done")
    
    # Test that adding a duplicate provider raises ValueError
    with pytest.raises(ValueError, match="Multiple tasks provide the same data"):
        @workflow.task(provides=["data"])
        async def task2(context):
            pass
    
    context = await workflow.execute()
    assert context.get("data") == "done"

# Empty Workflow Test
async def test_empty_workflow():
    workflow = Workflow("test_empty")
    context = await workflow.execute()
    assert isinstance(context, Context)

# Complex Dependency Chain
async def test_complex_dependency_chain():
    workflow = Workflow("test_complex")
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
    
    context = await workflow.execute()
    assert execution_order == ["a", "b", "c", "d"]
    assert context.get("result") == "aabc"

# Cleanup Test
async def test_context_cleanup():
    workflow = Workflow("test_cleanup")
    
    @workflow.task(provides=["temp"])
    async def task1(context):
        context.set("temp", "temporary")
    
    @workflow.task(requires=["temp"])
    async def task2(context):
        assert context.get("temp") == "temporary"
        context.clear()
    
    context = await workflow.execute()
    assert len(context._data) == 0

# Task Timeout Test
async def test_task_timeout():
    workflow = Workflow("test_timeout")
    
    @workflow.task()
    async def long_running_task(context):
        await asyncio.sleep(10)  # Simulate long task
    
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.1):
            await workflow.execute()

# Task Cancellation Test
async def test_task_cancellation():
    workflow = Workflow("test_cancel")
    was_cancelled = False
    
    @workflow.task()
    async def cancellable_task(context):
        nonlocal was_cancelled
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            was_cancelled = True
            raise
    
    task = asyncio.create_task(workflow.execute())
    await asyncio.sleep(0.1)
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task
    
    assert was_cancelled
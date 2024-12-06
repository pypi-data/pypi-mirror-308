import pytest
from src import CircularDependencyError, DependencyNotFoundError
from src.utils.validation import validate_dag
from src.core.task import Task
from src.core.context import Context

def test_validate_complex_dag():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, provides=["data1"]),
        "task2": Task(task_func, requires=["data1"], provides=["data2"]),
        "task3": Task(task_func, requires=["data2"], provides=["data3"]),
        "task4": Task(task_func, requires=["data1", "data3"])
    }
    
    validate_dag(tasks, context)

def test_validate_self_dependency():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, provides=["data1"], requires=["data1"])
    }
    
    with pytest.raises(CircularDependencyError):
        validate_dag(tasks, context)

def test_validate_multiple_dependencies():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, requires=["nonexistent1", "nonexistent2"])
    }
    
    with pytest.raises(DependencyNotFoundError) as exc:
        validate_dag(tasks, context)
    # Should mention both missing dependencies in error message
    assert "nonexistent1" in str(exc.value)
    assert "nonexistent2" in str(exc.value) 

def test_validate_circular_dependency_complex():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, provides=["data1"]),
        "task2": Task(task_func, requires=["data1"], provides=["data2"]),
        "task3": Task(task_func, requires=["data2"], provides=["data3"]),
        "task4": Task(task_func, requires=["data3"], provides=["data1"])
    }
    
    with pytest.raises(CircularDependencyError):
        validate_dag(tasks, context)

def test_validate_empty_tasks():
    context = Context()
    validate_dag({}, context)

def test_validate_no_dependencies():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, provides=["data1"]),
        "task2": Task(task_func, provides=["data2"]),
        "task3": Task(task_func, provides=["data3"])
    }
    
    validate_dag(tasks, context)

def test_validate_multiple_providers():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, provides=["data1"]),
        "task2": Task(task_func, provides=["data1"]),  # Multiple tasks provide same data
        "task3": Task(task_func, requires=["data1"])
    }
    
    validate_dag(tasks, context)

def test_validate_complex_circular():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(task_func, provides=["data1"]),
        "task2": Task(task_func, requires=["data3"], provides=["data2"]),
        "task3": Task(task_func, requires=["data2"], provides=["data3"]),
        "task4": Task(task_func, requires=["data1", "data2"])
    }
    
    with pytest.raises(CircularDependencyError):
        validate_dag(tasks, context)

def test_validate_disconnected_components():
    def task_func(context): pass
    context = Context()
    tasks = {
        # Component 1
        "task1": Task(task_func, provides=["data1"]),
        "task2": Task(task_func, requires=["data1"], provides=["data2"]),
        # Component 2 (disconnected)
        "task3": Task(task_func, provides=["data3"]),
        "task4": Task(task_func, requires=["data3"], provides=["data4"])
    }
    
    validate_dag(tasks, context)

def test_validate_complex_branching():
    def task_func(context): pass
    context = Context()
    tasks = {
        "root": Task(task_func, provides=["root_data"]),
        "branch1_1": Task(task_func, requires=["root_data"], provides=["b1_data"]),
        "branch1_2": Task(task_func, requires=["b1_data"], provides=["b1_final"]),
        "branch2_1": Task(task_func, requires=["root_data"], provides=["b2_data"]),
        "branch2_2": Task(task_func, requires=["b2_data"], provides=["b2_final"]),
        "merger": Task(task_func, requires=["b1_final", "b2_final"], provides=["final"])
    }
    
    validate_dag(tasks, context)
from typing import Dict, Set
from ..core.task import Task
from ..exceptions.workflow_exceptions import CircularDependencyError, DependencyNotFoundError
from ..core.context import Context

def validate_dag(tasks: Dict[str, Task], context: Context) -> None:
    """Validate that the workflow forms a valid DAG based on data dependencies."""
    # Track all available data keys from tasks and context
    available_keys: Set[str] = set()
    
    # Add keys from existing context data
    with context._lock:
        available_keys.update(context._data.keys())
    
    # Add keys provided by tasks
    for task in tasks.values():
        available_keys.update(task.provides)
    
    # Check that all required keys will be provided
    for task_name, task in tasks.items():
        missing_keys = task.requires - available_keys
        if missing_keys:
            raise DependencyNotFoundError(
                f"Task '{task_name}' requires keys {missing_keys} which are not provided by any task"
            )
    
    # Check for circular dependencies
    visited: Set[str] = set()
    temp: Set[str] = set()
    
    def visit(task_name: str) -> None:
        if task_name in temp:
            raise CircularDependencyError(f"Circular dependency detected involving {task_name}")
        if task_name in visited:
            return
        
        temp.add(task_name)
        task = tasks[task_name]
        # Find all tasks that provide the required keys
        for req_key in task.requires:
            for dep_name, dep_task in tasks.items():
                if req_key in dep_task.provides:
                    visit(dep_name)
        temp.remove(task_name)
        visited.add(task_name)
    
    for task_name in tasks:
        visit(task_name)
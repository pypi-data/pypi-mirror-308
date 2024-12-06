from typing import Dict, List, Set
from functools import wraps
import asyncio
from .context import Context
from .task import Task
from ..models.types import TaskFunction, TaskStatus
from ..utils.validation import validate_dag
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class Workflow:
    """Manages the execution of tasks in a DAG."""
    def __init__(self, name: str, context: Context):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.context = context
        logger.info(f"Created workflow: {name}")
    
    def task(
        self,
        requires: List[str] = None,
        provides: List[str] = None
    ) -> callable:
        """Decorator to register a task in the workflow."""
        def decorator(func: TaskFunction) -> callable:
            task = Task(func, requires, provides)
            
            # Check for duplicate provides
            for existing_task in self.tasks.values():
                duplicate_provides = set(task.provides) & set(existing_task.provides)
                if duplicate_provides:
                    raise ValueError(
                        f"Multiple tasks provide the same data: {duplicate_provides}. "
                        f"Tasks: {task.name} and {existing_task.name}"
                    )
            
            self.tasks[task.name] = task
            logger.debug(f"Registered task: {task.name}")
            
            return func
        return decorator
    
    def _get_ready_tasks(self, completed: Set[str]) -> List[Task]:
        """Get tasks whose dependencies are satisfied."""
        ready = []
        for task in self.tasks.values():
            # Check if task is pending
            if task.status != TaskStatus.PENDING:
                continue
                
            # Get all provided data keys from completed tasks AND existing context data
            available_data = set(self.context.keys())
            for completed_task in self.tasks.values():
                if completed_task.name in completed:
                    available_data.update(completed_task.provides)
                    
            # Check if all required data is available
            if task.requires.issubset(available_data):
                ready.append(task)
                
        return ready
    
    async def execute(self) -> None:
        """Execute the workflow."""
        logger.info(f"Starting workflow execution: {self.name}")
        validate_dag(self.tasks, self.context)
        completed_tasks: Set[str] = set()
        
        while len(completed_tasks) < len(self.tasks):
            ready_tasks = self._get_ready_tasks(completed_tasks)
            if not ready_tasks:
                remaining = [t.name for t in self.tasks.values() 
                           if t.status != TaskStatus.COMPLETED]
                logger.error(f"No tasks ready to execute. Remaining: {remaining}")
                raise RuntimeError(f"No tasks ready to execute. Remaining: {remaining}")
            
            tasks = [task.execute(self.context) for task in ready_tasks]
            await asyncio.gather(*tasks)
            
            for task in ready_tasks:
                task.status = TaskStatus.COMPLETED
                completed_tasks.add(task.name)
        
        logger.info(f"Completed workflow execution: {self.name}")
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
        
    async def cleanup(self):
        """Cleanup workflow resources."""
        self.context.clear()
        # Add any additional cleanup
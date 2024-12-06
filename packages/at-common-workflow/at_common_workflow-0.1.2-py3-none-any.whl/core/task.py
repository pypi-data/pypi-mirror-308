from typing import List, Set
import asyncio
from ..models.types import TaskStatus, TaskFunction
from ..utils.logging import setup_logger
from .context import Context

logger = setup_logger(__name__)

class Task:
    """Represents a single task in the workflow."""
    def __init__(
        self,
        func: TaskFunction,
        requires: List[str] = None,
        provides: List[str] = None
    ):
        self.name = func.__name__
        self.func = func
        self.requires: Set[str] = set(requires or [])
        self.provides: Set[str] = set(provides or [])
        self.status = TaskStatus.PENDING
    
    async def execute(self, context: Context) -> None:
        """Execute the task function."""
        try:
            self.status = TaskStatus.RUNNING
            logger.info(f"Starting task: {self.name}")
            
            if not asyncio.iscoroutinefunction(self.func):
                raise ValueError(f"Task {self.name} must be an async function")
            
            await self.func(context)
            
            self.status = TaskStatus.COMPLETED
            logger.info(f"Completed task: {self.name}")
            
        except Exception as e:
            self.status = TaskStatus.FAILED
            logger.error(f"Task {self.name} failed: {str(e)}")
            raise
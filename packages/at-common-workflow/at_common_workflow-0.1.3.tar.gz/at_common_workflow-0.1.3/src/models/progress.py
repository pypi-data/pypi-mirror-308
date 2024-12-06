from dataclasses import dataclass
from .types import TaskProgressStatus

@dataclass
class TaskProgress:
    """Represents the progress status of a task in the workflow."""
    name: str
    status: TaskProgressStatus 
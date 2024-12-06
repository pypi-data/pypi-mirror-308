from enum import Enum
from typing import Any, Dict, List, Set, Callable

class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

TaskFunction = Callable[['Context'], Any]
DataDict = Dict[str, Any]
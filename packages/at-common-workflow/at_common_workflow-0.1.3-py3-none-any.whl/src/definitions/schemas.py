from typing import Dict, List, Any
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional

@dataclass
class TaskParameter:
    type: str
    default: Any = None
    required: bool = True

class TaskDefinition(BaseModel):
    """Defines a task's configuration and dependencies.
    
    Attributes:
        name: Unique identifier for the task
        module: Fully qualified module path containing the task function
        function: Name of the async function to execute
        parameters: Configuration parameters to pass to the function
        requires: List of data keys required by this task
        provides: List of data keys this task will produce
    """
    name: str
    module: str
    function: str
    parameters: Optional[Dict[str, Any]] = None
    requires: Optional[List[str]] = []
    provides: Optional[List[str]] = []

class WorkflowDefinition(BaseModel):
    name: str
    tasks: List[TaskDefinition]
    initial_context: Optional[Dict[str, Any]] = None
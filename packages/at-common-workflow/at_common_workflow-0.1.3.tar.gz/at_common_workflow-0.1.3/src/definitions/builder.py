from typing import Dict, Any
from ..core.workflow import Workflow
from ..core.context import Context
from .loader import TaskLoader
from .schemas import WorkflowDefinition, TaskDefinition
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class WorkflowBuilder:
    """Builds workflows from JSON definitions."""
    
    @classmethod
    def from_json(
        cls,
        definition: Dict[str, Any],
        context: Context
    ) -> Workflow:
        """Create a workflow from JSON definition."""
        try:
            workflow_def = WorkflowDefinition(**definition)
            workflow = Workflow(workflow_def.name, context)
            
            # Initialize context with initial values if provided
            if workflow_def.initial_context:
                for key, value in workflow_def.initial_context.items():
                    context.set(key, value)
                logger.debug(f"Initialized context with: {workflow_def.initial_context.keys()}")
            
            # Create tasks
            for task_def in workflow_def.tasks:
                func = TaskLoader.load_function(
                    task_def.module,
                    task_def.function
                )
                
                task = TaskLoader.create_wrapped_task(
                    func=func,
                    parameters=task_def.parameters,
                    requires=task_def.requires,
                    provides=task_def.provides
                )
                
                task.name = task_def.name
                workflow.tasks[task.name] = task
                logger.debug(f"Added task {task.name} to workflow {workflow.name}")
            
            return workflow
            
        except Exception as e:
            logger.error(f"Error building workflow: {str(e)}")
            raise

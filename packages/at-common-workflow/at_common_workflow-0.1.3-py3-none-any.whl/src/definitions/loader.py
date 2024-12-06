from typing import Any, Dict, Callable, List
import importlib
import inspect
from ..core.context import Context
from ..core.task import Task
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class TaskLoader:
    """Handles dynamic loading and wrapping of task functions."""
    
    @staticmethod
    def load_function(module_path: str, function_name: str) -> Callable:
        try:
            module = importlib.import_module(module_path)
            func = getattr(module, function_name)
            
            if not inspect.iscoroutinefunction(func):
                raise ValueError(f"Function {function_name} must be async")
                
            return func
        except ImportError:
            logger.error(f"Could not import module: {module_path}")
            raise
        except AttributeError:
            logger.error(f"Function {function_name} not found in {module_path}")
            raise

    @staticmethod
    def create_wrapped_task(
        func: Callable,
        parameters: Dict[str, Any],
        requires: List[str],
        provides: List[str]
    ) -> Task:
        if not inspect.iscoroutinefunction(func):
            raise ValueError(f"Function {func.__name__} must be async")
        
        async def wrapped(context: Context) -> None:
            sig = inspect.signature(func)
            kwargs = {}
            
            for param_name, param in sig.parameters.items():
                if param_name == 'context':
                    kwargs['context'] = context
                elif param_name in parameters:
                    kwargs[param_name] = parameters[param_name]
                elif param.default == inspect.Parameter.empty:
                    raise ValueError(f"Required parameter {param_name} not provided")
            
            await func(**kwargs)
        
        return Task(wrapped, requires, provides)

from threading import Lock
from typing import Any, Dict, List, TypeVar, Generic
import copy
from ..models.types import DataDict

T = TypeVar('T')

class Context(Generic[T]):
    """Thread-safe workflow context that stores data shared between tasks."""
    def __init__(self):
        self._data: DataDict = {}
        self._lock = Lock()
        self._write_locks: Dict[str, Lock] = {}
    
    def get(self, key: str, default: T = None) -> T:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        with self._lock:
            value = copy.deepcopy(self._data.get(key, default))
            return value
    
    def set(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        with self._lock:
            if key not in self._write_locks:
                self._write_locks[key] = Lock()
        
        with self._write_locks[key]:
            with self._lock:
                self._data[key] = copy.deepcopy(value)

    def delete(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        with self._lock:
            if key in self._data:
                if key not in self._write_locks:
                    self._write_locks[key] = Lock()
                
                with self._write_locks[key]:
                    del self._data[key]
                    del self._write_locks[key]
    
    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self._write_locks.clear()
    
    def __contains__(self, key: str) -> bool:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        with self._lock:
            return key in self._data
    
    def keys(self) -> List[str]:
        """Returns a list of all keys in the context."""
        with self._lock:
            return list(self._data.keys())
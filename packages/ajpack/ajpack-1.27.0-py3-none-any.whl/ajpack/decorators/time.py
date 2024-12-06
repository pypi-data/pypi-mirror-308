import time
from typing import Any

def log_execution_time(decimals: int = 4) -> Any:
    def start_function(func) -> Any:
        def wrapper(*args, **kwargs) -> Any:
            start_time: float = time.time()
            result: Any = func(*args, **kwargs)
            end_time: float = time.time()
            execution_time: float = end_time - start_time
            print(f"Function '{func.__name__}' executed in {execution_time:.{decimals}f} seconds")
            return result
        return wrapper
    return start_function

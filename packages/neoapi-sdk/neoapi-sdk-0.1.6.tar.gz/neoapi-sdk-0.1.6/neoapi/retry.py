import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Union

logger = logging.getLogger(__name__)

T = TypeVar('T')

def with_retries(
    max_retries: int = 3,
    retry_delay: float = 5.0,
    exceptions: tuple = (Exception,),
    is_async: bool = False
) -> Callable:
    """Decorator to add retry logic to any function."""
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if is_async:
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Optional[Exception] = None
                
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt + 1 < max_retries:
                            logger.warning(
                                f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}"
                                f" - Retrying in {retry_delay} seconds..."
                            )
                            await asyncio.sleep(retry_delay)
                        else:
                            logger.error(f"Max retries ({max_retries}) reached")
                            raise last_exception
                
                if last_exception:
                    raise last_exception
                return None  # Should never reach here
            
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Optional[Exception] = None
                
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt + 1 < max_retries:
                            logger.warning(
                                f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}"
                                f" - Retrying in {retry_delay} seconds..."
                            )
                            time.sleep(retry_delay)
                        else:
                            logger.error(f"Max retries ({max_retries}) reached")
                            raise last_exception
                
                if last_exception:
                    raise last_exception
                return None  # Should never reach here
            
            return sync_wrapper
    
    return decorator
import asyncio
import functools
import logging
import warnings
from typing import Any, Callable, Optional, TypeVar, Union, cast

from .client_async import NeoApiClientAsync
from .client import NeoApiClient
from .models import LLMOutput

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Callable[..., Any])

def track_llm_output(
    client=None,
    model_name=None,
    prompt=None,
    output=None,
    metadata=None,
    return_analysis=False,
    project="default_project",
    group="default_group",
    analysis_slug=None,
    need_analysis_response=False,
    format_json_output=False,
    save_text=True,
):
    if client and isinstance(client, NeoApiClientAsync):
        warnings.warn("Async client used in sync context", RuntimeWarning, stacklevel=2)

    def decorator(func):
        def sync_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if not client or isinstance(client, NeoApiClientAsync):
                return result

            try:
                llm_output = LLMOutput(
                    text=str(output if output else result),
                    model_name=model_name,
                    prompt=prompt() if callable(prompt) else prompt,
                    metadata=metadata,
                    project=project,
                    group=group,
                    analysis_slug=analysis_slug,
                    need_analysis_response=need_analysis_response,
                    format_json_output=format_json_output,
                    save_text=save_text
                )
                client.track(llm_output)
            except Exception as e:
                logger.error(f"Failed to track output: {str(e)}")

            return result

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            try:
                if client:
                    llm_output = LLMOutput(
                        text=str(output if output else result),
                        model_name=model_name,
                        prompt=prompt() if callable(prompt) else prompt,
                        metadata=metadata,
                        project=project,
                        group=group,
                        analysis_slug=analysis_slug,
                        need_analysis_response=need_analysis_response,
                        format_json_output=format_json_output,
                        save_text=save_text
                    )
                    await client.track(llm_output)
            except Exception as e:
                logger.error(f"Failed to track output: {str(e)}")

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

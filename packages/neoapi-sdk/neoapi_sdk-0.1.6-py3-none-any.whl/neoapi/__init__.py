# __init__.py

from .client import NeoApiClient
from .client_async import NeoApiClientAsync
from .client_sync import NeoApiClientSync
from .decorators import track_llm_output, track_llm_output_async
from .models import LLMOutput

__all__ = [
    "NeoApiClient",
    "NeoApiClientAsync",
    "NeoApiClientSync",
    "track_llm_output",
    "track_llm_output_async",
    "LLMOutput",
]

# Type aliases for better type checking
from typing import Union, TypeAlias

AsyncClient: TypeAlias = Union[NeoApiClient, NeoApiClientAsync]
SyncClient: TypeAlias = Union[NeoApiClient, NeoApiClientSync]

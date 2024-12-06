import asyncio
import json
import logging
import os
import threading
import time
from typing import List, Optional

import aiohttp
import requests

from .config import Config
from .exceptions import NeoApiError
from .models import LLMOutput

logger = logging.getLogger(__name__)

class NeoApiClient:
    """
    Unified Client for interacting with the Neo API to send LLM outputs.
    Works in both synchronous and asynchronous contexts.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        batch_size: int = 10,
        flush_interval: float = 5.0,
        max_retries: int = 3,
        api_url: Optional[str] = None,
        check_frequency: int = 1,
        timeout: float = 10.0,
    ):
        api_key = api_key or os.environ.get("NEOAPI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key must be provided either directly or through NEOAPI_API_KEY environment variable."
            )
        
        self.api_key = api_key
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.max_retries = max_retries
        self.timeout = timeout
        self.api_url = (api_url or Config.API_URL).rstrip("/")
        self.check_frequency = check_frequency

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Sync attributes
        self._sync_queue: List[LLMOutput] = []
        self._sync_lock = threading.Lock()
        self._sync_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._sync_session: Optional[requests.Session] = None
        
        # Async attributes
        self._async_queue: List[LLMOutput] = []
        self._async_lock: Optional[asyncio.Lock] = None
        self._async_task: Optional[asyncio.Task] = None
        self._async_session: Optional[aiohttp.ClientSession] = None
        
        self._is_async = False

    def __enter__(self):
        """Sync context manager entry."""
        self.start_sync()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit."""
        self.stop_sync()

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start_async()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop_async()

    def start_sync(self) -> None:
        """Start the client in synchronous mode."""
        if self._sync_session is None:
            self._sync_session = requests.Session()
            self._sync_session.headers.update(self.headers)
            self._stop_event.clear()
            self._sync_thread = threading.Thread(
                target=self._periodic_flush_sync, daemon=True
            )
            self._sync_thread.start()

    async def start_async(self) -> None:
        """Start the client in asynchronous mode."""
        self._is_async = True
        if self._async_session is None:
            self._async_session = aiohttp.ClientSession(headers=self.headers)
            self._async_lock = asyncio.Lock()
            self._async_task = asyncio.create_task(self._periodic_flush_async())

    def stop_sync(self) -> None:
        """Stop the synchronous client."""
        self._stop_event.set()
        if self._sync_thread and self._sync_thread.is_alive():
            self._sync_thread.join(timeout=self.flush_interval + 1)
        self.flush_sync()
        if self._sync_session:
            self._sync_session.close()

    async def stop_async(self) -> None:
        """Stop the asynchronous client."""
        if self._async_task:
            self._async_task.cancel()
            try:
                await self._async_task
            except asyncio.CancelledError:
                pass
        await self.flush_async()
        if self._async_session:
            await self._async_session.close()

    def track(self, llm_output: LLMOutput) -> None:
        """Track an LLM output synchronously."""
        if self._is_async:
            raise RuntimeError("Cannot use sync track in async context. Use track_async instead.")
        
        with self._sync_lock:
            self._sync_queue.append(llm_output)
            if len(self._sync_queue) >= self.batch_size:
                self.flush_sync()

    async def track_async(self, llm_output: LLMOutput) -> None:
        """Track an LLM output asynchronously."""
        if not self._is_async:
            raise RuntimeError("Cannot use async track in sync context. Use track instead.")
        
        if self._async_lock is None:
            raise RuntimeError("Async lock not initialized. Call start_async() first.")
            
        async with self._async_lock:
            self._async_queue.append(llm_output)
            if len(self._async_queue) >= self.batch_size:
                await self.flush_async()

    async def atrack(self, llm_output: LLMOutput) -> None:
        """Unified async track method."""
        await self.track_async(llm_output)

    def flush_sync(self) -> None:
        """Flush the synchronous queue."""
        with self._sync_lock:
            if not self._sync_queue:
                return
            batch = self._sync_queue.copy()
            self._sync_queue.clear()
            self._send_batch_sync(batch)

    async def flush_async(self) -> None:
        """Flush the asynchronous queue."""
        if self._async_lock is None:
            raise RuntimeError("Async lock not initialized. Call start_async() first.")
            
        async with self._async_lock:
            if not self._async_queue:
                return
            batch = self._async_queue.copy()
            self._async_queue.clear()
            await self._send_batch_async(batch)

    def _periodic_flush_sync(self) -> None:
        while not self._stop_event.is_set():
            time.sleep(self.flush_interval)
            self.flush_sync()

    async def _periodic_flush_async(self) -> None:
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush_async()

    def _send_batch_sync(self, batch: List[LLMOutput]) -> None:
        """Send a batch of LLM outputs synchronously."""
        if not self._sync_session:
            raise RuntimeError("Sync session not initialized")

        for item in batch:
            self._post_item_sync(item)

    async def _send_batch_async(self, batch: List[LLMOutput]) -> None:
        """Send a batch of LLM outputs asynchronously."""
        if not self._async_session:
            raise RuntimeError("Async session not initialized")

        tasks = [self._post_item_async(item) for item in batch]
        await asyncio.gather(*tasks)

    async def _post_item_async(self, item: LLMOutput) -> None:
        """Post a single item asynchronously."""
        if not self._async_session:
            raise RuntimeError("Async session not initialized")

        url = f"{self.api_url}/{'analyze' if item.need_analysis_response else 'save'}"
        payload = item.model_dump()

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with self._async_session.post(url, json=payload, timeout=timeout) as response:
                if response.status == 401:
                    text = await response.text()
                    logger.error(f"Authentication failed: {text}")
                    raise NeoApiError(f"Authentication failed: {text}")
                elif response.status >= 400:
                    text = await response.text()
                    logger.error(f"API request failed: {text}")
                    raise NeoApiError(f"Error {response.status}: {text}")
                elif item.need_analysis_response:
                    try:
                        analysis_response = await response.json()
                        if item.format_json_output:
                            formatted_response = json.dumps(analysis_response, indent=4)
                            logger.info(f"Analysis Response:\n{formatted_response}")
                        else:
                            logger.info(f"Analysis Response: {analysis_response}")
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON from analysis response")
                else:
                    logger.debug("Successfully sent item")
        except aiohttp.ClientError as e:
            logger.error(f"Network error while sending item: {e}")
            raise
        except asyncio.TimeoutError:
            logger.error("Request timed out")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while sending item: {e}")
            raise

    def _post_item_sync(self, item: LLMOutput) -> None:
        """Post a single item synchronously."""
        if not self._sync_session:
            raise RuntimeError("Sync session not initialized")

        url = f"{self.api_url}/{'analyze' if item.need_analysis_response else 'save'}"
        payload = item.model_dump()

        try:
            response = self._sync_session.post(
                url, 
                json=payload,
                timeout=self.timeout
            )
            if response.status_code == 401:
                logger.error(f"Authentication failed: {response.text}")
                raise NeoApiError(f"Authentication failed: {response.text}")
            response.raise_for_status()
            
            if item.need_analysis_response:
                try:
                    analysis_response = response.json()
                    if item.format_json_output:
                        formatted_response = json.dumps(analysis_response, indent=4)
                        logger.info(f"Analysis Response:\n{formatted_response}")
                    else:
                        logger.info(f"Analysis Response: {analysis_response}")
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON from analysis response")
            else:
                logger.debug("Successfully sent item")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while sending item: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while sending item: {e}")
            raise
"""
Fetch content from the internet.
"""

import asyncio
from collections.abc import Callable, Awaitable
from dataclasses import dataclass
from json import loads
from logging import getLogger
from pathlib import Path
from time import time
from typing import Any

from aiohttp import ClientSession, ClientResponse, ClientError
from multidict import CIMultiDict

from betty.cache import Cache, CacheItemValueT
from betty.cache.file import BinaryFileCache
from betty.error import UserFacingError
from betty.hashid import hashid
from betty.locale import Str


class FetchError(UserFacingError, RuntimeError):
    """
    An error that occurred when fetching a URL.
    """

    pass  # pragma: no cover


@dataclass
class FetchResponse:
    """
    An HTTP response.
    """

    headers: CIMultiDict[str]
    body: bytes
    encoding: str

    @property
    def text(self) -> str:
        """
        The body as plain text.

        This may raise an error if the response body cannot be represented as plain text.
        """
        return self.body.decode(self.encoding)

    @property
    def json(self) -> Any:
        """
        The body as JSON.

        This may raise an error if the response body cannot be represented as JSON or plain text.
        """
        return loads(self.text)


class Fetcher:
    """
    Fetch content from the internet.
    """

    def __init__(
        self,
        http_client: ClientSession,
        response_cache: Cache[FetchResponse],
        binary_file_cache: BinaryFileCache,
        # Default to seven days.
        ttl: int = 86400 * 7,
    ):
        self._response_cache = response_cache
        self._binary_file_cache = binary_file_cache
        self._ttl = ttl
        self._http_client = http_client
        self._logger = getLogger(__name__)

    async def _fetch(
        self,
        url: str,
        cache: Cache[CacheItemValueT],
        response_mapper: Callable[[ClientResponse], Awaitable[CacheItemValueT]],
    ) -> tuple[CacheItemValueT, str]:
        cache_item_id = hashid(url)

        response_data: CacheItemValueT | None = None
        async with cache.getset(cache_item_id) as (cache_item, setter):
            if cache_item and cache_item.modified + self._ttl > time():
                response_data = await cache_item.value()
            else:
                self._logger.debug(f'Fetching "{url}"...')
                try:
                    async with self._http_client.get(url) as response:
                        response_data = await response_mapper(response)
                except ClientError as error:
                    self._logger.warning(
                        f'Could not successfully connect to "{url}": {error}'
                    )
                except asyncio.TimeoutError:
                    self._logger.warning(f'Timeout when connecting to "{url}"')
                else:
                    await setter(response_data)

        if response_data is None:
            if cache_item:
                response_data = await cache_item.value()
            else:
                raise FetchError(
                    Str.plain(
                        f'Could neither fetch "{url}", nor find an old version in the cache.'
                    )
                )

        return response_data, cache_item_id

    async def _map_response(self, response: ClientResponse) -> FetchResponse:
        return FetchResponse(
            response.headers.copy(),
            await response.read(),
            response.get_encoding(),
        )

    async def fetch(self, url: str) -> FetchResponse:
        """
        Fetch an HTTP resource.
        """
        response_data, _ = await self._fetch(
            url, self._response_cache, self._map_response
        )
        return response_data

    async def fetch_file(self, url: str) -> Path:
        """
        Fetch a file.

        :return: The path to the file on disk.
        """
        _, cache_item_id = await self._fetch(
            url, self._binary_file_cache, ClientResponse.read
        )
        return self._binary_file_cache.cache_item_file_path(cache_item_id)

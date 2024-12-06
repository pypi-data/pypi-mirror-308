
import os
import httpx
import asyncio
import typing as _typing
import logging as logging2
logging2.basicConfig(level=logging2.INFO)
from concurrent.futures import ThreadPoolExecutor

from KeyisBLogging import logging

from .Exceptions import Exceptions
from .core import DNS, ProtocolsManager
from .models import Url, Request, Response








class AsyncClient:
    def __init__(self):
        pass

    async def get(self,
                url: _typing.Union[Url, str],
                data=None,
                json: _typing.Optional[dict] = None,
                headers=None) -> Response:
        return await self.request("GET", url=url, data=data, json=json, headers=headers)

    async def request(self,
                      method: str,
                      url: _typing.Union[Url, str],
                      data: _typing.Mapping[str, _typing.Any] | None = None,
                      json: dict | None = None,
                      protocolVersion: _typing.Optional[str] = None,
                      **kwargs,
                      ) -> Response:
        if isinstance(url, str):
            url = Url(url)
        logging.info(f'Url -> {url}')

        request = Request(
            method,
            url,
            data=data,
            json=json
            )
        

        return await ProtocolsManager.requestAsync(request)

        


    # async def stream(self, method: str, url: str, **kwargs) -> AsyncGenerator[httpx.Response, None]:
    #     # Логируем начало стриминга
    #     logging.info(f"Streaming request: {method} {url} | Params: {kwargs.get('params')}")
    #     try:
    #         async with self._client.stream(method, url, **kwargs) as response:
    #             # Логируем успешный стриминг
    #             logging.info(f"Streaming response [{response.status_code}] started for {url}")
    #             yield response
    #     except Exception as e:
    #         # Логируем ошибку стриминга
    #         logging.error(f"Streaming request failed: {method} {url} | Error: {str(e)}")
    #         raise
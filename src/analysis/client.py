import httpx
from typing import Any, Dict, Optional
from json_repair import json_repair
import asyncio
import logging
from src.config import Settings

_logger = logging.getLogger(__name__)

class Singleton(type):
    """Singleton metaclass to ensure only one instance of the class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AnalysisClient(metaclass=Singleton):
    """ The client analysis client, which handles all the external API class, to supp.ai, the food data API as well as the openAi API """
    _retries = Settings().api_retries if Settings().api_retries is not None else 3

    @classmethod
    async def _request(cls, request_url: str, method: str, data: Optional[Any], parameters: Optional[Dict[str, str]], headers: Optional[Dict[str, str]]) -> Optional[httpx.Response]:
        response = None
        status_code = "no_code_assigned_yet"
        async with httpx.AsyncClient() as client:
            for attempts in range(cls._retries):
                try:
                    response = await getattr(client, method.lower())(url=request_url, **{key: value for key, value in
                            {
                                "params": parameters,
                                "data": data,
                                "headers": headers,
                            }.items() if value})

                    status_code = response.status_code
                    response.raise_for_status()

                    return response

                except httpx.HTTPStatusError:
                    _logger.warning(f"Attempt {attempts + 1}/{cls._retries}: HTTP status error for {request_url} with status code {status_code}", exc_info=True, )

                    if attempts + 1 >= cls._retries:
                        _logger.error(f"Max retries reached for {request_url}.")
                        raise

                except (httpx.RequestError, asyncio.TimeoutError) as exc:
                    _logger.warning(f"Attempt {attempts + 1}/{cls._retries}: Request or timeout error for {request_url}: {str(exc)}",exc_info=True, )

                    if attempts + 1 >= cls._retries:
                        _logger.error(f"Max retries reached for {request_url}.")
                        raise

                except Exception as exc:
                    _logger.error(f"Unexpected error during request to {request_url}: {type(exc).__name__}: {exc}", exc_info=True, )
                    raise

        return None

if __name__ == "__main__":
    async def main():
        #response1 = await AnalysisClient()._request("https://supp.ai/api/agent/search", "get", None, {"q": "ginkgo"}, None)
        #if response1:
            #print("Response for ginkgo:", response1.json())
        print("not live")

    asyncio.run(main())

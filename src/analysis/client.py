import httpx
from typing import Any, Dict, Optional, Union, List, Tuple
from json_repair import json_repair
from json import JSONDecodeError
import asyncio
import logging
from json_repair.json_parser import JSONReturnType
from src.config import Settings

#TODO: make this better
_logger = logging.getLogger(__name__)

class Singleton(type):
    """Singleton metaclass to ensure only one instance of the class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#TODO:
class AnalysisClient(metaclass=Singleton):
    """ The client analysis class, which handles all the external API class, to supp.ai, the food data API as well as the openAi API """
    _retries = Settings().api_retries if Settings().api_retries is not None else 3
    _number_of_pages = Settings().number_of_pages if Settings().number_of_pages is not None else 1
    _agent_interaction_uri = Settings().agent_interaction_uri if Settings().agent_interaction_uri is not None else None
    CLIENT = httpx.AsyncClient()

    @classmethod
    async def _request(cls, request_url: str, method: str, data: Optional[Any], parameters: Optional[Dict[str, str]], headers: Optional[Dict[str, str]]) -> Optional[httpx.Response]:
        response = None
        status_code = "no_code_assigned_yet"
        for attempts in range(cls._retries):
            try:
                response = await getattr(cls.CLIENT, method.lower())(url=request_url,
                    **{key: value for key, value in
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

    @staticmethod
    def _response_to_json(response: Optional[httpx.Response]) -> Optional[Union[JSONReturnType, Tuple[JSONReturnType, List[Dict[str, str]]]]]:
        try:
            if response:
                return json_repair.repair_json(response.json())

            raise TypeError(f"Response format: {type(response)} could not be parsed into JSON")

        except JSONDecodeError:
            #retry somehow...
            ...

        except TypeError as exc:
            _logger.error(f"Unexpected value of response: {type(response)} during the json processing: {type(exc).__name__}: {exc}", exc_info=True, )
            raise

        except Exception as exc:
            _logger.error(f"Unexpected error during the json processing of {response}: {type(exc).__name__}: {exc}", exc_info=True, )
            raise

    #TODO: first check in the DB if this agent has been searched before, make a random chance that it still searches
    #TODO: save the search result if none has been save, or if random has took effect see if its the same, else replace by the newer version
    #TODO: add things to actually only get the relevant parts. But I do not know them yet!
    @classmethod
    async def get_agent_interaction(cls, agent: str) -> Optional[Union[JSONReturnType, Tuple[JSONReturnType, List[Dict[str, str]]]]]:
        if cls._agent_interaction_uri:
            try:
                response = cls._response_to_json(
                    await cls._request(cls._agent_interaction_uri, "get", None, {"q": agent}, None)
                )

                return response
            except Exception:
                ...
        else:
            return None

    @classmethod
    async def get_nutrients(cls, products: List[str]) -> Optional[Union[JSONReturnType, Tuple[JSONReturnType, List[Dict[str, str]]]]]:
        ...

if __name__ == "__main__":
    async def main():
        #response1 = await AnalysisClient()._request("https://supp.ai/api/agent/search", "get", None, {"q": "ginkgo"}, None)
        #if response1:
            #print("Response for ginkgo:", response1.json())
        print("not live")

    asyncio.run(main())

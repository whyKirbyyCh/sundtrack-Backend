import httpx
from typing import Any, Dict, Optional
from json_repair import json_repair

class Singleton(type):
    """Singleton metaclass to ensure only one instance of the class exists."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AnalysisClient(metaclass=Singleton):
    """ The client analysis client, which handles all the external API class, to supp.ai, the food data API as well as the openAi API """

    @staticmethod
    async def _request(request_url: str, method: str, data: Optional[Any], parameters: Optional[Dict[str, str]], header: Optional[Dict[str, str]]) -> Optional[httpx.Response]:
        response = None

        with httpx.Client() as client:
            try:
                response = getattr(client, method)(url=request_url, parameters=parameters, header=header, data=data)
            except:
                pass


        return response

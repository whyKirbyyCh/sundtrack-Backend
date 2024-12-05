import motor.motor_asyncio
from src.config import Settings
from typing import Optional, List, Dict, Any, Union
import logging

_logger = logging.getLogger(__name__)

class Database:
    """ The class which handles the connections to the database """

    def __init__(self) -> None:
        self._client = motor.motor_asyncio.AsyncIOMotorClient(Settings().database_uri)

    def __enter__(self) -> Optional[motor.motor_asyncio.AsyncIOMotorClient]:
        if not self._client:
            try:
                self._client = motor.motor_asyncio.AsyncIOMotorClient(Settings().database_uri)

            except Exception:
                raise

            finally:
                return None

        return self._client

    def __exit__(self) -> None:
        try:
            self._client.close()

        except Exception as exc:
            _logger.error(f"Unexpected error while closing the connection to the database: {type(exc).__name__}: {exc}", exc_info=True, )

    async def insert(self, collection_name: str, documents: List[Dict[str, Any]], database_name: str = Settings().main_database) -> Optional[Any]:
        try:
            database = self._client[database_name]
            collection = database[collection_name]

            if isinstance(documents, list) and all(isinstance(document, dict) for document in documents):
                if len(documents) == 1:
                    result = await collection.insert_one(documents[0])

                elif len(documents) >= 1:
                    result = await database.collection.insert_many([documents])

                else:
                    result = None

            else:
                raise TypeError(f"Tried to insert document of a wrong type: {type(documents[0])}, or from a wrong collection {type(documents)}")

            return result

        except Exception:
            ...

    async def retrieve(self, collection_name: str, query: Dict[str, Any], multiple: bool = False, amount: Optional[int] = None, database_name: str = Settings().main_database) -> Union[Optional[Dict[str, Any]], List[Optional[Dict[str, Any]]]]:
        try:
            database = self._client[database_name]
            collection = database[collection_name]

            if not multiple:
                document = await collection.find_one(query)
                return document

            else:
                documents = collection.find(query)
                return await documents.to_list(length=amount)

        except Exception:
            ...

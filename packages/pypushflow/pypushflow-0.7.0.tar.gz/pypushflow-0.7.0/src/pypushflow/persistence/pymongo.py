from typing import Mapping, Any

try:
    import bson
    import pymongo
    from bson.objectid import ObjectId
except Exception:
    bson = None
    pymongo = None
    ObjectId = None
from .mongo import MongoWorkflowDbClient


class PyMongoWorkflowDbClient(MongoWorkflowDbClient, register_name="pymongo"):
    """Client of an external Mongo database for storing workflow executions."""

    def __init__(self, url: str, database: str, collection: str):
        super().__init__()
        self._url = url
        self._database = database
        self._collection = collection

    def connect(self):
        if pymongo is None:
            return
        client = pymongo.MongoClient(self._url, serverSelectionTimeoutMS=10000)
        self._client = client
        self._collection = client[self._database][self._collection]

    def disconnect(self):
        self._collection = None
        if self._client is not None:
            self._client.close()
            self._client = None

    def generateWorkflowId(self) -> ObjectId:
        return ObjectId()

    def generateActorId(self) -> ObjectId:
        return ObjectId()

    def _appendActorInfo(self, actorInfo: dict):
        self._safe_update_one(
            {"_id": self._workflowId}, {"$push": {"actors": actorInfo}}
        )

    def _sanitize(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {k: self._sanitize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [self._sanitize(v) for v in value]
        if not any(isinstance(value, t) for t in bson._BUILT_IN_TYPES):
            return repr(value)
        return value

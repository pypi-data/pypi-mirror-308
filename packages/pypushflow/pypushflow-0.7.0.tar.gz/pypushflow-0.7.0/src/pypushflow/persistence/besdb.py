from .pymongo import PyMongoWorkflowDbClient

try:
    from bson.objectid import ObjectId
except Exception:
    ObjectId = None


class BesWorkflowDbClient(PyMongoWorkflowDbClient, register_name="besdb"):
    """Client of the BES Mongo database for storing workflow executions."""

    def __init__(self, url: str, initiator: str, host: str, port: int, request_id: str):
        self._request_id = ObjectId(str(request_id))

        self._initial_workflow_info = {
            "_id": self._request_id,
            "initiator": str(initiator),
            "host": str(host),
            "port": str(port),
            "Request ID": str(request_id),
        }

        super().__init__(url, "bes", "bes")

    def _generateInitialWorkflowInfo(self) -> dict:
        return dict(self._initial_workflow_info)

    def generateWorkflowId(self) -> ObjectId:
        return self._request_id

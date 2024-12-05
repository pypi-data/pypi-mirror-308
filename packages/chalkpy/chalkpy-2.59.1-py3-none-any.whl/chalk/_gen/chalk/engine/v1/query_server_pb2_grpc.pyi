"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from abc import (
    ABCMeta,
    abstractmethod,
)
from chalk._gen.chalk.aggregate.v1.service_pb2 import (
    GetAggregatesRequest,
    GetAggregatesResponse,
    PlanAggregateBackfillRequest,
    PlanAggregateBackfillResponse,
)
from chalk._gen.chalk.common.v1.online_query_pb2 import (
    OnlineQueryBulkRequest,
    OnlineQueryBulkResponse,
    OnlineQueryMultiRequest,
    OnlineQueryMultiResponse,
    OnlineQueryRequest,
    OnlineQueryResponse,
    UploadFeaturesBulkRequest,
    UploadFeaturesBulkResponse,
)
from chalk._gen.chalk.engine.v1.query_server_pb2 import (
    PingRequest,
    PingResponse,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    UnaryUnaryMultiCallable,
)

class QueryServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    Ping: UnaryUnaryMultiCallable[
        PingRequest,
        PingResponse,
    ]
    OnlineQuery: UnaryUnaryMultiCallable[
        OnlineQueryRequest,
        OnlineQueryResponse,
    ]
    OnlineQueryBulk: UnaryUnaryMultiCallable[
        OnlineQueryBulkRequest,
        OnlineQueryBulkResponse,
    ]
    OnlineQueryMulti: UnaryUnaryMultiCallable[
        OnlineQueryMultiRequest,
        OnlineQueryMultiResponse,
    ]
    UploadFeaturesBulk: UnaryUnaryMultiCallable[
        UploadFeaturesBulkRequest,
        UploadFeaturesBulkResponse,
    ]
    PlanAggregateBackfill: UnaryUnaryMultiCallable[
        PlanAggregateBackfillRequest,
        PlanAggregateBackfillResponse,
    ]
    """PlanAggregateBackfill determines the estimated resources needed to backfill
    an aggregate.

    This method is a duplicate of the PlanAggregateBackfill method
    in the query_server.proto file. We should remove the query_server.proto method
    and move that request to this service instead.
    buf:lint:ignore RPC_REQUEST_RESPONSE_UNIQUE
    """
    GetAggregates: UnaryUnaryMultiCallable[
        GetAggregatesRequest,
        GetAggregatesResponse,
    ]
    """This method is a duplicate of the PlanAggregateBackfill method
    in the query_server.proto file. We should remove the query_server.proto method
    and move that request to this service instead.
    buf:lint:ignore RPC_REQUEST_RESPONSE_UNIQUE
    """

class QueryServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def Ping(
        self,
        request: PingRequest,
        context: ServicerContext,
    ) -> PingResponse: ...
    @abstractmethod
    def OnlineQuery(
        self,
        request: OnlineQueryRequest,
        context: ServicerContext,
    ) -> OnlineQueryResponse: ...
    @abstractmethod
    def OnlineQueryBulk(
        self,
        request: OnlineQueryBulkRequest,
        context: ServicerContext,
    ) -> OnlineQueryBulkResponse: ...
    @abstractmethod
    def OnlineQueryMulti(
        self,
        request: OnlineQueryMultiRequest,
        context: ServicerContext,
    ) -> OnlineQueryMultiResponse: ...
    @abstractmethod
    def UploadFeaturesBulk(
        self,
        request: UploadFeaturesBulkRequest,
        context: ServicerContext,
    ) -> UploadFeaturesBulkResponse: ...
    @abstractmethod
    def PlanAggregateBackfill(
        self,
        request: PlanAggregateBackfillRequest,
        context: ServicerContext,
    ) -> PlanAggregateBackfillResponse:
        """PlanAggregateBackfill determines the estimated resources needed to backfill
        an aggregate.

        This method is a duplicate of the PlanAggregateBackfill method
        in the query_server.proto file. We should remove the query_server.proto method
        and move that request to this service instead.
        buf:lint:ignore RPC_REQUEST_RESPONSE_UNIQUE
        """
    @abstractmethod
    def GetAggregates(
        self,
        request: GetAggregatesRequest,
        context: ServicerContext,
    ) -> GetAggregatesResponse:
        """This method is a duplicate of the PlanAggregateBackfill method
        in the query_server.proto file. We should remove the query_server.proto method
        and move that request to this service instead.
        buf:lint:ignore RPC_REQUEST_RESPONSE_UNIQUE
        """

def add_QueryServiceServicer_to_server(servicer: QueryServiceServicer, server: Server) -> None: ...

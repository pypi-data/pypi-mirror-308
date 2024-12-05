"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from abc import (
    ABCMeta,
    abstractmethod,
)
from chalk._gen.chalk.server.v1.billing_pb2 import (
    GetNodesAndPodsRequest,
    GetNodesAndPodsResponse,
    GetUsageChartRequest,
    GetUsageChartResponse,
    GetUtilizationRatesRequest,
    GetUtilizationRatesResponse,
)
from chalk._gen.chalk.server.v1.pod_request_pb2 import (
    GetPodRequestChartsRequest,
    GetPodRequestChartsResponse,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    UnaryUnaryMultiCallable,
)

class BillingServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    GetNodesAndPods: UnaryUnaryMultiCallable[
        GetNodesAndPodsRequest,
        GetNodesAndPodsResponse,
    ]
    """GetNodesAndPods returns the nodes and pods for the team by default,
    not just a single environment. To limit the scope, add filters to
    the request object.
    """
    GetUsageChart: UnaryUnaryMultiCallable[
        GetUsageChartRequest,
        GetUsageChartResponse,
    ]
    """GetUsageChart shows the Chalk credit usage between a provided start and
    end period. The usage can be grouped by UsageChartPeriod for daily or
    monthly usage, and by UsageChartGrouping for instance type or cluster usage.
    """
    GetUtilizationRates: UnaryUnaryMultiCallable[
        GetUtilizationRatesRequest,
        GetUtilizationRatesResponse,
    ]
    """GetUtilizationRates returns the current utilization rates for all
    instance types.
    """
    GetPodRequestCharts: UnaryUnaryMultiCallable[
        GetPodRequestChartsRequest,
        GetPodRequestChartsResponse,
    ]

class BillingServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def GetNodesAndPods(
        self,
        request: GetNodesAndPodsRequest,
        context: ServicerContext,
    ) -> GetNodesAndPodsResponse:
        """GetNodesAndPods returns the nodes and pods for the team by default,
        not just a single environment. To limit the scope, add filters to
        the request object.
        """
    @abstractmethod
    def GetUsageChart(
        self,
        request: GetUsageChartRequest,
        context: ServicerContext,
    ) -> GetUsageChartResponse:
        """GetUsageChart shows the Chalk credit usage between a provided start and
        end period. The usage can be grouped by UsageChartPeriod for daily or
        monthly usage, and by UsageChartGrouping for instance type or cluster usage.
        """
    @abstractmethod
    def GetUtilizationRates(
        self,
        request: GetUtilizationRatesRequest,
        context: ServicerContext,
    ) -> GetUtilizationRatesResponse:
        """GetUtilizationRates returns the current utilization rates for all
        instance types.
        """
    @abstractmethod
    def GetPodRequestCharts(
        self,
        request: GetPodRequestChartsRequest,
        context: ServicerContext,
    ) -> GetPodRequestChartsResponse: ...

def add_BillingServiceServicer_to_server(servicer: BillingServiceServicer, server: Server) -> None: ...

import json
import pandas as pd
from typing import Union, Dict, Iterable, List

from ..._core.session import get_default, raise_if_closed
from ..._tools import convert_df_columns_to_datetime
from ...usage_collection._logger import get_usage_logger
from ...usage_collection._utils import ModuleName
from ...usage_collection._filter_types import FilterType
from ...delivery import endpoint_request
from ..._tools._datetime import convert_to_datetime

pre_trade_forecast_default_fields = [
    "ArrivalTime",
    "Symbol",
    "OrderQuantityUSD",
    "CostOfLiquidity",
    "RiskTransferBPS",
    "ArrivalVolatilityPct",
    "ForecastModel",
    "ForecastPerfBPS",
    "ForecastPerfStdErr",
    "ForecastDurationMins",
    "ForecastDurationStdErr",
    "ForecastRiskBPS",
    "AlphaBPS",
    "InformationRatio",
    "RunsToBeatRT95",
    "RunsToBeatRT85",
]

pre_trade_forecast_default_forecast_models = ["tradefeedr/Global", "tradefeedr/Fast", "tradefeedr/Slow"]

parent_orders_default_fields = [
    "Date",
    "ParentOrderID",
    "Symbol",
    "TradeCurrency",
    "Side",
    "LegSymbols",
    "Trader",
    "Account",
    "SubAccount",
    "AlgoName",
    "LP",
    "TimeZoneArrive",
    "HourArrive",
    "TimeZoneEnd",
    "HourEnd",
    "G10EM",
    "TradeSizeBucketUSDM",
    "OrderQuantity",
    "AvgChildOrderQuantityUSD",
    "OrderQuantityUSD",
    "TradeQuantityUSD",
    "TradeQuantity",
    "RemainQuantity",
    "ArrivalTime",
    "ArrivalPrice",
    "TWAPPrice",
    "LastTime",
    "LastPrice",
    "NumChildEvents",
    "NumParentEvents",
    "CurrencyPositions",
    "Duration",
    "TradeIntensity",
    "OrderIntensity",
    "RiskTransferPrice",
    "PrincipalMid",
    "DailyVolatilityPct",
    "ArrivalVolatilityPct",
    "SpreadPaidPMChildOrders",
    "AllInPrice",
    "AllInNetPrice",
    "ExecutionScore",
    "ReversalScore",
    "RiskTransferCostReportedPM",
    "RiskTransferCostStaticPM",
    "RiskTransferCostVolBumpPM",
    "RiskTransferCostModelPM",
    "RiskTransferCostTradefeedrPM",
    "AssumedRisk",
    "ArrivalMidPerfTradeBPS",
    "ArrivalMidPerfRemainBPS",
    "ArrivalMidPerfBPS",
    "TWAPMidPerfBPS",
    "ArrivalMidPerfNetBPS",
    "ArrivalMidPerfTradeNetBPS",
    "ArrivalMidPerfRemainNetBPS",
    "TWAPMidPerfNetBPS",
    "SlippageToArrivalMidTradePM",
    "SlippageToArrivalMidRemainPM",
    "SlippageToArrivalMidPM",
    "SlippageToTWAPMidPM",
    "SlippageToArrivalMidNetPM",
    "SlippageToArrivalMidTradeNetPM",
    "SlippageToArrivalMidRemainNetPM",
    "SlippageToTWAPMidNetPM",
    "SubmissionTime",
    "SubmissionPrice",
    "FirstFillTime",
    "FirstFillPrice",
    "SubmissionMidPerfBPS",
    "SubmissionMidPerfTradeBPS",
    "SubmissionMidPerfRemainBPS",
    "SubmissionMidPerfNetBPS",
    "SubmissionMidPerfTradeNetBPS",
    "SubmissionMidPerfRemainNetBPS",
    "FirstFillMidPerfBPS",
    "FirstFillMidPerfTradeBPS",
    "FirstFillMidPerfRemainBPS",
    "FirstFillMidPerfNetBPS",
    "FirstFillMidPerfTradeNetBPS",
    "FirstFillMidPerfRemainNetBPS",
]


class TradefeedrError(Exception):
    """Base class for exceptions in this module."""

    pass


class BadRequestError(TradefeedrError):
    pass


class UnauthorizedError(TradefeedrError):
    pass


class ForbiddenError(TradefeedrError):
    pass


class NotFoundError(TradefeedrError):
    pass


class MethodNotAllowedError(TradefeedrError):
    pass


class UnsupportedMediaTypeError(TradefeedrError):
    pass


class TooManyRequestsError(TradefeedrError):
    pass


class InternalServerError(TradefeedrError):
    pass


class BadGatewayError(TradefeedrError):
    pass


class ServiceUnavailableError(TradefeedrError):
    pass


class GatewayTimeoutError(TradefeedrError):
    pass


class InputSizeMismatchError(TradefeedrError):
    pass


def ensure_list(arg: Union[str, int, float, Iterable[Union[str, int, float]]]) -> List[Union[str, int, float]]:
    if isinstance(arg, (str, int, float)):
        return [arg]
    return list(arg)


def check_input_sizes(universe, order_quantity_usd, arrival_time):
    if not (len(universe) == len(order_quantity_usd) == len(arrival_time)):
        raise InputSizeMismatchError(
            "The the number of items under universe, order_quantity_usd, and arrival_time must be the same."
        )


def handle_response(response) -> pd.DataFrame:
    if response.raw.status_code == 200:
        if type(response.data.raw) is str:
            response_json = json.loads(response.data.raw)
            response.data.df = pd.DataFrame(response_json["result"])
        else:
            response.data.df = pd.DataFrame(response.data.raw["result"])
        convert_df_columns_to_datetime(response.data.df, "ArrivalTime", utc=True, delete_tz=True, unit="ms")
        return response.data.df
    elif response.raw.status_code == 400:
        raise BadRequestError("Bad Request: The server could not understand the request due to invalid syntax.")
    elif response.raw.status_code == 401:
        raise UnauthorizedError("Unauthorized: The client must authenticate itself to get the requested response.")
    elif response.raw.status_code == 403:
        raise ForbiddenError("Forbidden: The client does not have access rights to the content.")
    elif response.raw.status_code == 404:
        raise NotFoundError("Not Found: The server can not find the requested resource.")
    elif response.raw.status_code == 405:
        raise MethodNotAllowedError(
            "Method Not Allowed: The request method is known by the server but has been disabled and cannot be used."
        )
    elif response.raw.status_code == 415:
        raise UnsupportedMediaTypeError(
            "Unsupported Media Type: The media format of the requested data is not supported by the server."
        )
    elif response.raw.status_code == 429:
        raise TooManyRequestsError("Too Many Requests: The user has sent too many requests in a given amount of time.")
    elif response.raw.status_code == 500:
        raise InternalServerError(
            "Internal Server Error: The server has encountered a situation it doesn't know how to handle."
        )
    elif response.raw.status_code == 502:
        raise BadGatewayError(
            "Bad Gateway: The server, while acting as a gateway or proxy, received an invalid response from the upstream server."
        )
    elif response.raw.status_code == 503:
        raise ServiceUnavailableError("Service Unavailable: The server is not ready to handle the request.")
    elif response.raw.status_code == 504:
        raise GatewayTimeoutError(
            "Gateway Timeout: The server is acting as a gateway or proxy and did not get a response in time."
        )
    else:
        raise TradefeedrError(f"Unexpected Error: {response.raw.status_code} - {response.raw}")


def get_fx_algo_pre_trade_forecast(
    universe: Union[str, Iterable[str]],
    order_quantity_usd: Union[float, int, Iterable[float], Iterable[int]],
    arrival_time: Union[str, Iterable[str]],
    fields: Union[str, Iterable[str], None] = None,
    forecast_model: Union[str, Iterable[str], None] = None,
) -> pd.DataFrame:
    """
    Fetches pre-trade forecast for given parameters.

    Parameters
    ----------
    universe: str | list
        Instrument(s) to request.
    order_quantity_usd: float | Iterable[float]
        List of order quantities in USD.
    arrival_time: str | Iterable[str]
        Arrival time(s).
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2024-01-20T15:04:05'.
    fields: str | Iterable[str], optional
        Field(s) to request.
    forecast_model: str | Iterable[str], optional
        Forecast model(s). Possible values are "tradefeedr/Global", "tradefeedr/Fast", "tradefeedr/Slow".

    Returns
    -------
    pd.DataFrame

    Examples
    --------
    >>> import lseg.data as ld
    >>> ld.tradefeedr.get_fx_algo_pre_trade_forecast(
    ...     universe=["EURUSD", "USDJPY"],
    ...     order_quantity_usd=[50e6, 30e6],
    ...     arrival_time=["2023-08-10 11:52", "2023-08-10 12:30"]
    ... )
    """

    universe = ensure_list(universe)
    order_quantity_usd = ensure_list(order_quantity_usd)
    arrival_time = ensure_list(arrival_time)
    check_input_sizes(universe, order_quantity_usd, arrival_time)
    arrival_time = [convert_to_datetime(time).strftime("%Y-%m-%dT%H:%M:%S") for time in arrival_time]
    fields = ensure_list(fields) if fields else pre_trade_forecast_default_fields
    forecast_model = ensure_list(forecast_model) if forecast_model else pre_trade_forecast_default_forecast_models

    req_filter = [
        {
            "function": "in",
            "var": "ForecastModel",
            "pars": forecast_model,
        },
    ]

    session = get_default()
    raise_if_closed(session)

    get_usage_logger().log_func(
        name=f"{ModuleName.ACCESS}.get_fx_algo_pre_trade_forecast",
        func_path=f"{__name__}.get_fx_algo_pre_trade_forecast",
        kwargs=dict(
            arrival_time=arrival_time,
            symbol=universe,
            order_quantity_usd=order_quantity_usd,
            fields=fields,
            filter=req_filter,
        ),
        desc={FilterType.SYNC, FilterType.LAYER_ACCESS},
    )

    request = endpoint_request.Definition(
        method=endpoint_request.RequestMethod.POST,
        url="tradefeedr/v1/fx/algo/pre-trade-forecast",
        header_parameters={"Content-Type": "application/json"},
        body_parameters={
            "options": {
                "select": fields,
                "filter": req_filter,
                "data": {"ArrivalTime": arrival_time, "Symbol": universe, "OrderQuantityUSD": order_quantity_usd},
            }
        },
    )

    response = request.get_data()
    return handle_response(response)


def get_fx_algo_parent_orders(
    start: str, end: str, fields: Union[str, Iterable[str], None] = None, extended_params: Union[None, Dict] = None
) -> pd.DataFrame:
    """
    Fetches parent orders for given parameters.

    Parameters
    ----------
    start: str
        Start of the period to get data for
    end: str
        End of the period to get data for
    fields: str | Iterable[str], optional
        Field(s) to request.
    extended_params: None | Dict, optional
        extra paremeters for the backend request

    Returns
    -------
    pd.Dataframe

    Examples
    --------
    >>> import lseg.data as ld
    >>> ld.tradefeedr.get_fx_algo_pre_trade_forecast(
    ...     start='2020-01-01',
    ...     end='2024-01-01'
    ... )
    """

    fields = ensure_list(fields) if fields else parent_orders_default_fields

    if isinstance(start, str):
        start = convert_to_datetime(start).strftime("%Y-%m-%d")
    else:
        start = [convert_to_datetime(time).strftime("%Y-%m-%d") for time in start]

    if isinstance(end, str):
        end = convert_to_datetime(end).strftime("%Y-%m-%d")
    else:
        end = [convert_to_datetime(time).strftime("%Y-%m-%d") for time in end]

    # if extended_params is None:
    tradefeedr_filter = [{"function": "within", "var": "Date", "pars": [start, end]}]

    # Staying consistent with the other LDL functions, we would like users
    # to be able to use `extended_params` as a direct JSON injector in the
    # call to LSEG's Data Platform. However, all Tradefeedr JSON request
    # bodies start with `'options'`; to simplify things, we allow users to
    # describe their `extended_params` with or without this parent object
    # `'options'` defined:
    if (
        extended_params and "options" not in extended_params
    ):  # This line checks if the highest key in the `extended_params` dictionary is 'options'.
        extended_params = {"options": extended_params}

    # If `extended_params` is provided, merge it with the default filter
    if extended_params and "options" in extended_params and "filter" in extended_params["options"]:
        # # Check if the first filter in extended_params is a date
        # # range that should overwrite `start` and `end`. We want `extended_params` to take
        # # precedence over other arguments populated in the `get_parent_orders` function.
        first_filter = extended_params["options"]["filter"]
        # Find the index of the line with function as "within" using list comprehension
        index = next((i for i, line in enumerate(first_filter) if line["function"] == "within"), -1)

        # Date ranges are specified in "options" if the "function" is set to "within"
        # and "var" to "Date"
        if first_filter[index]["function"] == "within" and first_filter[index]["var"] == "Date":
            start, end = first_filter[index]["pars"]
            tradefeedr_filter = extended_params["options"]["filter"]
        else:
            tradefeedr_filter.extend(extended_params["options"]["filter"])

    # Send request to PPE RDP endpoint
    request = endpoint_request.Definition(
        method=endpoint_request.RequestMethod.POST,
        url="tradefeedr/v1/fx/algo/parent-orders",
        header_parameters={"Content-Type": "application/json"},
        body_parameters={"options": {"select": fields, "filter": tradefeedr_filter}},
    )

    response = request.get_data()

    return handle_response(response)

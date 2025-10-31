import reflex as rx
from typing import TypedDict, Literal


class OrderBookLevel(TypedDict):
    side: Literal["bid", "ask"]
    price: float
    size: int


class TradeFill(TypedDict):
    timestamp: str
    side: Literal["buy", "sell"]
    price: float
    size: int
    market_id: str


class StrategyParams(TypedDict):
    target_spread_bps: int
    max_inventory: int
    base_quote_size: int
    skew: float
    enabled: bool


class PriceDataPoint(TypedDict):
    time: str
    price: float


class Market(TypedDict):
    market_id: str
    ticker: str
    description: str
    best_bid: float | None
    best_ask: float | None
    my_bid_price: float | None
    my_bid_size: int | None
    my_ask_price: float | None
    my_ask_size: int | None
    inventory: int
    unrealized_pnl: float
    quoting_active: bool
    total_volume: int
    price_history: list[PriceDataPoint]
    strategy_params: StrategyParams
    order_book: list[OrderBookLevel]
    recent_trades: list[TradeFill]
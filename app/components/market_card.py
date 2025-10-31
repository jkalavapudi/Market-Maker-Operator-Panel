import reflex as rx
from app.state import BotState
from app.models import Market


def metric_item(label: str, value: rx.Var, unit: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.span(label, class_name="text-sm font-medium text-gray-500"),
        rx.el.div(
            rx.el.span(value, class_name="text-lg font-semibold text-gray-900"),
            rx.el.span(unit, class_name="text-sm text-gray-500 ml-1"),
            class_name="flex items-baseline",
        ),
        class_name="flex flex-col",
    )


def quote_display(side: str, price: rx.Var, size: rx.Var) -> rx.Component:
    color_class = rx.cond(side == "Bid", "text-green-600", "text-red-600")
    return rx.el.div(
        rx.el.span(f"My {side}", class_name=f"text-sm font-medium {color_class}"),
        rx.el.div(
            rx.el.span(
                rx.cond(price.is_none(), "-", price.to_string()),
                class_name="font-mono text-base font-semibold",
            ),
            rx.el.span(" x ", class_name="text-gray-400 mx-1"),
            rx.el.span(
                rx.cond(size.is_none(), "-", size.to_string()),
                class_name="font-mono text-base font-semibold",
            ),
            class_name="flex items-center text-gray-800",
        ),
        class_name="flex flex-col items-center p-2 rounded-lg",
    )


def market_card(market: Market) -> rx.Component:
    return rx.el.div(
        rx.link(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        market["description"],
                        class_name="font-semibold text-gray-800 hover:underline",
                    ),
                    rx.el.p(
                        market["ticker"], class_name="text-xs text-gray-500 truncate"
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        rx.cond(market["quoting_active"], "Active", "Paused"),
                        class_name=rx.cond(
                            market["quoting_active"],
                            "px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full",
                            "px-2 py-1 text-xs font-medium text-yellow-800 bg-yellow-100 rounded-full",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-start",
            ),
            href=f"/market/{market['market_id']}",
            on_click=lambda: BotState.set_active_market_id(market["market_id"]),
            class_name="p-4 border-b block",
        ),
        rx.el.div(
            metric_item("Best Bid", market["best_bid"], ""),
            metric_item("Best Ask", market["best_ask"], ""),
            metric_item("Inventory", market["inventory"], "shares"),
            rx.el.div(
                rx.el.span(
                    "Unrealized PNL", class_name="text-sm font-medium text-gray-500"
                ),
                rx.el.div(
                    rx.el.span(
                        rx.cond(market["unrealized_pnl"] >= 0, "+", "-"),
                        class_name=rx.cond(
                            market["unrealized_pnl"] >= 0,
                            "text-lg font-semibold text-green-600",
                            "text-lg font-semibold text-red-600",
                        ),
                    ),
                    rx.el.span("$", class_name="text-lg font-semibold"),
                    rx.el.span(
                        rx.cond(
                            market["unrealized_pnl"] < 0,
                            market["unrealized_pnl"] * -1,
                            market["unrealized_pnl"],
                        ),
                        class_name="text-lg font-semibold",
                    ),
                    class_name=rx.cond(
                        market["unrealized_pnl"] >= 0,
                        "flex items-baseline text-green-600",
                        "flex items-baseline text-red-600",
                    ),
                ),
                class_name="flex flex-col text-right",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 p-4",
        ),
        rx.el.div(
            quote_display("Bid", market["my_bid_price"], market["my_bid_size"]),
            rx.el.div(class_name="border-l h-12"),
            quote_display("Ask", market["my_ask_price"], market["my_ask_size"]),
            class_name="flex items-center justify-around bg-gray-50 p-2 rounded-b-lg",
        ),
        rx.el.div(
            rx.el.button(
                rx.cond(market["quoting_active"], "Pause Quoting", "Resume Quoting"),
                on_click=lambda: BotState.toggle_market_quoting(market["market_id"]),
                class_name=rx.cond(
                    market["quoting_active"],
                    "w-full h-8 text-xs bg-yellow-500 text-white rounded-md hover:bg-yellow-600",
                    "w-full h-8 text-xs bg-blue-500 text-white rounded-md hover:bg-blue-600",
                ),
            ),
            class_name="p-2",
        ),
        class_name="bg-white border rounded-lg shadow-sm hover:shadow-md transition-shadow",
    )
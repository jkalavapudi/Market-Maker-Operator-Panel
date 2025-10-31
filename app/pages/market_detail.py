import reflex as rx
from app.state import BotState
from app.models import OrderBookLevel, TradeFill
from app.components.sidebar import sidebar


def order_book_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Order Book", class_name="text-lg font-semibold text-gray-800 mb-2"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Price",
                            class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider p-2",
                        ),
                        rx.el.th(
                            "Size",
                            class_name="text-right text-xs font-medium text-gray-500 uppercase tracking-wider p-2",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        BotState.selected_market["order_book"],
                        lambda level: rx.el.tr(
                            rx.el.td(
                                level["price"],
                                class_name=f"p-2 font-mono text-sm {rx.cond(level['side'] == 'bid', 'text-green-600', 'text-red-600')}",
                            ),
                            rx.el.td(
                                level["size"],
                                class_name="p-2 font-mono text-sm text-right text-gray-700",
                            ),
                        ),
                    )
                ),
                class_name="w-full divide-y divide-gray-200",
            ),
            class_name="bg-white border rounded-lg shadow-sm p-4 h-96 overflow-y-auto",
        ),
    )


def recent_trades_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Recent Trades", class_name="text-lg font-semibold text-gray-800 mb-2"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Time",
                            class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider p-2",
                        ),
                        rx.el.th(
                            "Side",
                            class_name="text-left text-xs font-medium text-gray-500 uppercase tracking-wider p-2",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="text-right text-xs font-medium text-gray-500 uppercase tracking-wider p-2",
                        ),
                        rx.el.th(
                            "Size",
                            class_name="text-right text-xs font-medium text-gray-500 uppercase tracking-wider p-2",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        BotState.selected_market["recent_trades"],
                        lambda trade: rx.el.tr(
                            rx.el.td(
                                trade["timestamp"],
                                class_name="p-2 font-mono text-xs text-gray-600",
                            ),
                            rx.el.td(
                                trade["side"].capitalize(),
                                class_name=f"p-2 text-sm font-medium {rx.cond(trade['side'] == 'buy', 'text-green-600', 'text-red-600')}",
                            ),
                            rx.el.td(
                                trade["price"],
                                class_name="p-2 font-mono text-sm text-right text-gray-700",
                            ),
                            rx.el.td(
                                trade["size"],
                                class_name="p-2 font-mono text-sm text-right text-gray-700",
                            ),
                        ),
                    )
                ),
                class_name="w-full divide-y divide-gray-200",
            ),
            class_name="bg-white border rounded-lg shadow-sm p-4 h-96 overflow-y-auto",
        ),
    )


def strategy_params_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Strategy Parameters", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Target Spread (bps)",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    default_value=BotState.selected_market["strategy_params"][
                        "target_spread_bps"
                    ].to_string(),
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Max Inventory",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    default_value=BotState.selected_market["strategy_params"][
                        "max_inventory"
                    ].to_string(),
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Base Quote Size",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    default_value=BotState.selected_market["strategy_params"][
                        "base_quote_size"
                    ].to_string(),
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Apply Changes",
                class_name="w-full h-10 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700",
            ),
            class_name="bg-white border rounded-lg shadow-sm p-4",
        ),
    )


def time_range_button(label: str) -> rx.Component:
    is_active = BotState.chart_time_range == label
    return rx.el.button(
        label,
        on_click=lambda: BotState.set_chart_time_range(label),
        class_name=rx.cond(
            is_active,
            "px-3 py-1 text-sm font-medium text-white bg-blue-600 rounded-md",
            "px-3 py-1 text-sm font-medium text-gray-600 bg-gray-200 rounded-md hover:bg-gray-300",
        ),
    )


def price_history_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Price History", class_name="text-lg font-semibold text-gray-800"),
            rx.el.div(
                time_range_button("1D"),
                time_range_button("1W"),
                time_range_button("1M"),
                time_range_button("ALL"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", horizontal=True, vertical=False
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.x_axis(data_key="time"),
                rx.recharts.y_axis(domain=[0, 1]),
                rx.recharts.line(
                    type_="monotone",
                    data_key="price",
                    stroke="#8884d8",
                    active_dot=True,
                    dot=False,
                ),
                data=BotState.price_history_for_range,
                height=300,
                margin={"top": 5, "right": 20, "left": -10, "bottom": 5},
            ),
            class_name="bg-white border rounded-lg shadow-sm p-4 h-96",
        ),
    )


def market_detail_content() -> rx.Component:
    return rx.el.main(
        rx.cond(
            BotState.selected_market,
            rx.el.div(
                rx.el.header(
                    rx.el.div(
                        rx.el.h1(
                            BotState.selected_market["description"],
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            BotState.selected_market["ticker"],
                            class_name="text-sm text-gray-500 mt-1 font-mono",
                        ),
                    ),
                    rx.el.div(
                        rx.el.span("Total Volume", class_name="text-sm text-gray-500"),
                        rx.el.div(
                            rx.el.span("$", class_name="text-2xl font-semibold"),
                            rx.el.span(
                                BotState.selected_market["total_volume"].to_string(),
                                class_name="text-2xl font-semibold",
                            ),
                            class_name="flex items-baseline text-gray-800",
                        ),
                        class_name="text-right",
                    ),
                    class_name="p-4 border-b bg-white flex justify-between items-center",
                ),
                rx.el.div(price_history_chart(), class_name="p-4 md:p-6"),
                rx.el.div(
                    rx.el.div(
                        order_book_view(),
                        recent_trades_view(),
                        class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
                    ),
                    strategy_params_view(),
                    class_name="p-4 md:p-6 grid grid-cols-1 xl:grid-cols-3 gap-6",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "loader-circle", class_name="h-8 w-8 animate-spin text-blue-600"
                    ),
                    rx.el.p(
                        "Loading market data...",
                        class_name="text-center text-gray-500 font-medium mt-4",
                    ),
                    class_name="flex flex-col items-center justify-center h-64 bg-gray-100 rounded-lg",
                )
            ),
        ),
        class_name="ml-64 flex flex-col items-center h-screen bg-gray-50 font-['Lato']",
    )


def market_detail_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        market_detail_content(),
        class_name="min-h-screen w-full bg-gray-50 font-['Lato']",
    )
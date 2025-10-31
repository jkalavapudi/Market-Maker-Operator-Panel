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


def market_detail_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.cond(
                BotState.selected_market,
                rx.el.div(
                    rx.el.header(
                        rx.el.h1(
                            BotState.selected_market["ticker"],
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            BotState.selected_market["description"],
                            class_name="text-sm text-gray-600 mt-1",
                        ),
                        class_name="p-4 border-b bg-white",
                    ),
                    rx.el.div(
                        rx.el.div(
                            order_book_view(),
                            recent_trades_view(),
                            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
                        ),
                        strategy_params_view(),
                        class_name="p-4 md:p-6 grid grid-cols-1 xl:grid-cols-3 gap-6",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Select a market to view details."), class_name="p-6"
                ),
            )
        ),
        class_name="ml-64 flex flex-col h-screen bg-gray-50",
    )


def market_detail_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        market_detail_content(),
        class_name="min-h-screen w-full bg-gray-50 font-['Lato']",
    )
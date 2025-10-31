import reflex as rx
from app.state import BotState
from app.models import Market
from app.components.sidebar import sidebar
from app.components.market_card import market_card
from app.components.log_viewer import log_viewer
from app.components.kill_switch_dialog import kill_switch_dialog


def status_badge(label: str, status: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.span(f"{label}:", class_name="text-sm font-medium text-gray-500"),
        rx.el.div(
            class_name=rx.match(
                status,
                ("connected", "w-2 h-2 rounded-full bg-green-500"),
                ("unauthorized", "w-2 h-2 rounded-full bg-yellow-500"),
                ("failed", "w-2 h-2 rounded-full bg-red-500"),
                ("disconnected", "w-2 h-2 rounded-full bg-gray-400"),
                "w-2 h-2 rounded-full bg-gray-400",
            )
        ),
        rx.el.span(status.capitalize(), class_name="text-sm text-gray-600"),
        class_name="flex items-center gap-2",
    )


def dashboard_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-900"),
            rx.el.div(
                status_badge("Kalshi", BotState.connection_status["kalshi"]),
                status_badge("Polymarket", BotState.connection_status["polymarket"]),
                class_name="flex items-center gap-6 mt-2",
            ),
            class_name="flex flex-col items-start w-full",
        ),
        rx.el.input(
            placeholder="Search markets (e.g., INFL)",
            on_change=BotState.set_search_query.debounce(300),
            class_name="w-full max-w-sm px-3 py-2 text-sm bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("play", class_name="h-4 w-4 mr-2"),
                "Start Bot",
                on_click=BotState.start_bot,
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-blue-600 text-white shadow hover:bg-blue-600/90 h-9 px-4 py-2",
                disabled=BotState.is_bot_running,
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-4 w-4 mr-2"),
                "Refresh Markets",
                on_click=BotState.fetch_markets,
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-gray-500 text-white shadow-sm hover:bg-gray-600 h-9 px-4 py-2",
            ),
            rx.el.button(
                rx.icon("square", class_name="h-4 w-4 mr-2"),
                "Stop Bot",
                on_click=BotState.stop_bot,
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-gray-700 text-white shadow-sm hover:bg-gray-700/90 h-9 px-4 py-2",
                disabled=~BotState.is_bot_running,
            ),
            rx.el.button(
                rx.icon("shield-alert", class_name="h-4 w-4 mr-2"),
                "Kill Switch",
                on_click=BotState.toggle_kill_switch_dialog,
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-red-600 text-white shadow hover:bg-red-600/90 h-9 px-4 py-2",
                disabled=BotState.global_kill_switch_active,
            ),
            kill_switch_dialog(),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between p-4 border-b bg-white",
    )


def dashboard_content() -> rx.Component:
    return rx.el.main(
        dashboard_header(),
        rx.el.div(
            rx.cond(
                BotState.active_markets.length() > 0,
                rx.el.div(
                    rx.foreach(
                        BotState.active_markets, lambda market: market_card(market)
                    ),
                    class_name="grid gap-6 md:grid-cols-2 lg:grid-cols-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.match(
                            BotState.connection_status["kalshi"],
                            (
                                "disconnected",
                                rx.el.p(
                                    "Connecting to Kalshi API...",
                                    class_name="text-center text-gray-500 font-medium",
                                ),
                            ),
                            (
                                "failed",
                                rx.el.p(
                                    "Failed to connect to Kalshi. Please check your internet connection or API credentials in Settings.",
                                    class_name="text-center text-red-500 font-medium",
                                ),
                            ),
                            (
                                "connected",
                                rx.el.p(
                                    "No open markets found on Kalshi.",
                                    class_name="text-center text-gray-500 font-medium",
                                ),
                            ),
                            rx.el.p(
                                "Loading market data...",
                                class_name="text-center text-gray-500 font-medium",
                            ),
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Go to Settings",
                                class_name="mt-4 inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-blue-600 text-white shadow hover:bg-blue-700 h-9 px-4 py-2",
                            ),
                            href="/settings",
                        ),
                        class_name="flex flex-col items-center",
                    ),
                    class_name="flex items-center justify-center h-64 bg-gray-100 rounded-lg",
                ),
            ),
            log_viewer(),
            class_name="flex flex-col gap-6 p-4 md:p-6",
        ),
        class_name="ml-64 flex flex-col h-screen font-['Lato'] bg-gray-50",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        dashboard_content(),
        class_name="min-h-screen w-full bg-gray-50 font-['Lato']",
    )
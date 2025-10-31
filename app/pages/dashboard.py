import reflex as rx
from app.state import BotState
from app.models import Market
from app.components.sidebar import sidebar
from app.components.market_card import market_card
from app.components.log_viewer import log_viewer
from app.components.kill_switch_dialog import kill_switch_dialog


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.div(
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
            rx.el.div(
                rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-900"),
                rx.el.div(
                    status_badge(BotState.connection_status["kalshi"]),
                    status_badge(BotState.connection_status["polymarket"]),
                    class_name="flex items-center gap-6",
                ),
                class_name="flex items-center justify-between w-full",
            ),
            class_name="flex items-center gap-4",
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
            rx.el.div(
                rx.foreach(BotState.active_markets, lambda market: market_card(market)),
                class_name="grid gap-6 md:grid-cols-2 lg:grid-cols-3",
            ),
            log_viewer(),
            class_name="flex flex-col gap-6 p-4 md:p-6",
        ),
        class_name="ml-64 flex flex-col h-screen font-['Inter'] bg-gray-50",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        dashboard_content(),
        class_name="min-h-screen w-full bg-gray-50 font-['Inter']",
    )
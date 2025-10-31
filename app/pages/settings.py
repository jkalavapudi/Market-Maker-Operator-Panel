import reflex as rx
from app.state import BotState
from app.components.sidebar import sidebar


def settings_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1("Settings", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Manage API credentials for exchanges.",
                class_name="text-sm text-gray-600 mt-1",
            ),
            class_name="p-4 border-b bg-white",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Kalshi API Credentials",
                    class_name="text-lg font-semibold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "API Key", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        default_value=BotState.kalshi_api_key,
                        on_change=BotState.set_kalshi_api_key,
                        placeholder="Enter your Kalshi API key",
                        type="password",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Secret Key",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        default_value=BotState.kalshi_secret_key,
                        on_change=BotState.set_kalshi_secret_key,
                        placeholder="Enter your Kalshi secret key",
                        type="password",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                    class_name="mb-4",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Polymarket API Credentials",
                    class_name="text-lg font-semibold text-gray-800 mb-4 mt-8",
                ),
                rx.el.div(
                    rx.el.label(
                        "API Key", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        default_value=BotState.polymarket_api_key,
                        on_change=BotState.set_polymarket_api_key,
                        placeholder="Enter your Polymarket API key",
                        type="password",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                ),
            ),
            rx.el.button(
                "Save Credentials",
                on_click=BotState.save_credentials,
                class_name="mt-8 w-full h-10 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700",
            ),
            class_name="p-4 md:p-6 bg-white border rounded-lg shadow-sm",
        ),
        class_name="ml-64 flex flex-col h-screen font-['Lato'] bg-gray-50 p-6",
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        settings_content(),
        class_name="min-h-screen w-full bg-gray-50 font-['Lato']",
    )
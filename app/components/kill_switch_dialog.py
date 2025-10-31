import reflex as rx
from app.state import BotState


def kill_switch_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Activate Global Kill Switch?", class_name="text-lg font-bold"
                ),
                rx.radix.primitives.dialog.description(
                    "This will immediately stop all quoting across all markets. This is an emergency action and should only be used to prevent critical losses.",
                    class_name="text-sm text-gray-600 mt-2",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            on_click=BotState.toggle_kill_switch_dialog,
                            class_name="mt-4 inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-gray-200 text-gray-800 shadow-sm hover:bg-gray-300 h-9 px-4 py-2",
                        )
                    ),
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "ACTIVATE KILL SWITCH",
                            on_click=BotState.activate_kill_switch,
                            class_name="mt-4 ml-3 inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-red-600 text-white shadow hover:bg-red-700 h-9 px-4 py-2",
                        )
                    ),
                    class_name="flex justify-end",
                ),
                class_name="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-md bg-white p-6 rounded-lg shadow-lg z-50",
            ),
        ),
        open=BotState.show_kill_switch_dialog,
        on_open_change=BotState.set_show_kill_switch_dialog,
    )
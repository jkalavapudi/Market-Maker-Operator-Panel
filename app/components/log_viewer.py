import reflex as rx
from app.state import BotState


def log_viewer() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Activity Log", class_name="text-lg font-semibold text-gray-800 px-4 pt-4"
        ),
        rx.el.div(
            rx.foreach(
                BotState.log_messages,
                lambda msg: rx.el.div(
                    rx.el.code(
                        msg["message"],
                        class_name=rx.match(
                            msg["level"],
                            ("info", "text-blue-500"),
                            ("warning", "text-yellow-600"),
                            ("error", "text-red-500"),
                            "text-gray-500",
                        ),
                    ),
                    class_name="font-mono text-xs px-4 py-1",
                ),
            ),
            class_name="h-48 overflow-y-scroll w-full font-mono text-xs",
        ),
        class_name="bg-white border rounded-lg shadow-sm mt-6",
    )
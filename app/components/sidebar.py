import reflex as rx
from app.state import BotState


def nav_item(text: str, href: str, icon: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(text),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-gray-900 transition-all hover:text-gray-900",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("bot", class_name="h-6 w-6 text-blue-600"),
                rx.el.span("Market Maker Bot", class_name="text-lg font-bold"),
                href="/",
                class_name="flex h-16 shrink-0 items-center gap-2 border-b px-4",
            ),
            rx.el.nav(
                nav_item("Dashboard", "/", "layout-dashboard", True),
                class_name="flex-1 overflow-auto py-2 flex flex-col gap-1 items-start px-4 text-sm font-medium",
            ),
        ),
        class_name="fixed left-0 top-0 h-full w-64 border-r bg-white z-10",
    )
import reflex as rx
from app.pages.dashboard import dashboard_page
from app.pages.market_detail import market_detail_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.state import BotState

app.add_page(dashboard_page, route="/")
app.add_page(
    market_detail_page,
    route="/market/[market_id]",
    on_load=BotState.on_load_market_detail,
)
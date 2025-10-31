import reflex as rx
import asyncio
from typing import Literal
from app.models import Market, OrderBookLevel, TradeFill, StrategyParams


class BotState(rx.State):
    is_bot_running: bool = False
    global_kill_switch_active: bool = False
    connection_status: dict[
        str, Literal["connected", "unauthorized", "failed", "disconnected"]
    ] = {"kalshi": "disconnected", "polymarket": "disconnected"}
    kalshi_api_key: str = rx.LocalStorage("", name="kalshi_api_key")
    kalshi_secret_key: str = rx.LocalStorage("", name="kalshi_secret_key")
    polymarket_api_key: str = rx.LocalStorage("", name="polymarket_api_key")
    markets: dict[str, Market] = {}
    active_market_id: str | None = None
    log_messages: list[dict[str, str]] = []
    show_kill_switch_dialog: bool = False
    search_query: str = ""

    @rx.var
    def active_markets(self) -> list[Market]:
        """Returns a list of all active markets, filtered by search query."""
        if not self.search_query:
            return list(self.markets.values())
        search_lower = self.search_query.lower()
        return [
            market
            for market in self.markets.values()
            if search_lower in market["ticker"].lower()
            or search_lower in market["description"].lower()
        ]

    @rx.var
    def selected_market(self) -> Market | None:
        """Returns the currently selected market for the detail view."""
        if self.active_market_id and self.active_market_id in self.markets:
            return self.markets[self.active_market_id]
        return None

    @rx.event
    def save_credentials(self):
        self._add_log("info", "API credentials saved.")
        rx.toast.success("Credentials saved!", duration=3000)
        if self.kalshi_api_key and self.kalshi_secret_key:
            self.connection_status["kalshi"] = "connected"
        else:
            self.connection_status["kalshi"] = "disconnected"
        if self.polymarket_api_key:
            self.connection_status["polymarket"] = "connected"
        else:
            self.connection_status["polymarket"] = "disconnected"

    @rx.event
    def toggle_kill_switch_dialog(self):
        self.show_kill_switch_dialog = not self.show_kill_switch_dialog

    @rx.event
    def activate_kill_switch(self):
        """Immediately stops all quoting."""
        self.global_kill_switch_active = True
        self.is_bot_running = False
        self._add_log(
            "error", "GLOBAL KILL SWITCH ACTIVATED. All quoting has been stopped."
        )
        self.show_kill_switch_dialog = False

    @rx.event
    def deactivate_kill_switch(self):
        """Resumes bot operation."""
        self.global_kill_switch_active = False
        self.is_bot_running = True
        self._add_log(
            "info", "Global kill switch deactivated. Bot resuming operations."
        )

    @rx.event
    def toggle_market_quoting(self, market_id: str):
        """Toggles the quoting status for a single market."""
        if market_id in self.markets:
            is_enabled = not self.markets[market_id]["quoting_active"]
            self.markets[market_id]["quoting_active"] = is_enabled
            self.markets[market_id]["strategy_params"]["enabled"] = is_enabled
            status = "enabled" if is_enabled else "disabled"
            self._add_log(
                "info",
                f"Quoting for market {self.markets[market_id]['ticker']} has been {status}.",
            )

    @rx.event
    def update_strategy_params(self, market_id: str, new_params: StrategyParams):
        """Updates strategy parameters for a market."""
        if market_id in self.markets:
            self.markets[market_id]["strategy_params"].update(new_params)
            self._add_log(
                "info",
                f"Strategy parameters for {self.markets[market_id]['ticker']} updated.",
            )
            rx.toast.info(
                f"Strategy updated for {self.markets[market_id]['ticker']}",
                duration=3000,
            )

    @rx.event
    def set_active_market_id(self, market_id: str):
        self.active_market_id = market_id

    @rx.event(background=True)
    async def on_load_dashboard(self):
        """Fetches markets when the dashboard loads."""
        async with self:
            if not self.markets:
                yield BotState.fetch_markets

    @rx.event(background=True)
    async def on_load_market_detail(self):
        """Ensure market data is loaded when navigating to detail page."""
        from app.kalshi_api import get_markets

        async with self:
            if not self.markets:
                yield BotState.fetch_markets
        async with self:
            market_id = self.router.page.params.get("market_id")
            if market_id and market_id in self.markets:
                self.active_market_id = market_id
            elif not self.active_market_id and self.markets:
                self.active_market_id = list(self.markets.keys())[0]

    @rx.event(background=True)
    async def poll_market_data(self):
        """Periodically polls the bot controller for fresh market data."""
        async with self:
            if not self.kalshi_api_key:
                self._add_log(
                    "error",
                    "Bot stopped. Kalshi API key not set. Please add it on the settings page.",
                )
                self.is_bot_running = False
                return
        while self.is_bot_running:
            await self.fetch_markets()
            await asyncio.sleep(5)

    @rx.event
    def start_bot(self):
        self.is_bot_running = True
        self._add_log("info", "Bot started. Initializing real-time data feeds.")
        return BotState.run_websocket_client

    @rx.event
    def stop_bot(self):
        self.is_bot_running = False
        self._add_log("warning", "Bot stopped. Disconnecting from real-time feeds.")

    def _add_log(self, level: str, message: str):
        """Adds a message to the log."""
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_messages.insert(
            0, {"level": level, "message": f"{timestamp} - {message}"}
        )
        if len(self.log_messages) > 100:
            self.log_messages.pop()

    @rx.event(background=True)
    async def fetch_markets(self):
        from app.kalshi_api import get_markets

        async with self:
            api_key = self.kalshi_api_key
            series_ticker = self.search_query if len(self.search_query) > 2 else None
        response_data = await get_markets(
            api_key, status="open", limit=500, series_ticker=series_ticker
        )
        async with self:
            if "error" in response_data:
                self._add_log("error", f"API Error: {response_data['error']}")
                self.connection_status["kalshi"] = "failed"
                return
            if api_key:
                self.connection_status["kalshi"] = "connected"
            raw_markets = response_data.get("markets", [])
            self._add_log("info", f"Fetched {len(raw_markets)} markets from Kalshi.")
            if raw_markets:
                self.markets.clear()
            strategy_template = {
                "target_spread_bps": 200,
                "max_inventory": 1000,
                "base_quote_size": 100,
                "skew": 0.5,
                "enabled": False,
            }
            for market_data in raw_markets:
                market_id = market_data["ticker"]
                if market_id not in self.markets:
                    self.markets[market_id] = Market(
                        market_id=market_id,
                        ticker=market_data["ticker"],
                        description=market_data["title"],
                        best_bid=market_data.get("yes_bid", 0) / 100.0,
                        best_ask=market_data.get("yes_ask", 0) / 100.0,
                        my_bid_price=None,
                        my_bid_size=None,
                        my_ask_price=None,
                        my_ask_size=None,
                        inventory=0,
                        unrealized_pnl=0.0,
                        quoting_active=False,
                        strategy_params=strategy_template.copy(),
                        order_book=[],
                        recent_trades=[],
                    )
                else:
                    self.markets[market_id]["best_bid"] = (
                        market_data.get("yes_bid", 0) / 100.0
                    )
                    self.markets[market_id]["best_ask"] = (
                        market_data.get("yes_ask", 0) / 100.0
                    )
            if not self.active_market_id and self.markets:
                self.active_market_id = list(self.markets.keys())[0]

    @rx.event(background=True)
    async def run_websocket_client(self):
        from app.websocket_client import KalshiWebsocketClient

        async with self:
            if not self.kalshi_api_key:
                self._add_log("error", "Cannot start bot: Kalshi API key is not set.")
                self.is_bot_running = False
                return
            market_tickers = list(self.markets.keys())
            if not market_tickers:
                self._add_log("warning", "No markets to monitor. Stopping bot.")
                self.is_bot_running = False
                return
            client = KalshiWebsocketClient(self.kalshi_api_key, market_tickers)
            yield
        await client.connect(self)
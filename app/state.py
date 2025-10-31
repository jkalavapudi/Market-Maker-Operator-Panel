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
    kalshi_api_key: str = ""
    kalshi_secret_key: str = ""
    polymarket_api_key: str = ""
    markets: dict[str, Market] = {}
    active_market_id: str | None = None
    log_messages: list[dict[str, str]] = []
    show_kill_switch_dialog: bool = False

    @rx.var
    def active_markets(self) -> list[Market]:
        """Returns a list of all active markets."""
        return list(self.markets.values())

    @rx.var
    def selected_market(self) -> Market | None:
        """Returns the currently selected market for the detail view."""
        if self.active_market_id and self.active_market_id in self.markets:
            return self.markets[self.active_market_id]
        return None

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
    async def on_load_market_detail(self):
        """Ensure market data is loaded when navigating to detail page."""
        async with self:
            if not self.markets:
                self._initialize_mock_data()
        async with self:
            market_id = self.router.page.params.get("market_id")
            if market_id and market_id in self.markets:
                self.active_market_id = market_id
            elif not self.active_market_id:
                if self.markets:
                    self.active_market_id = list(self.markets.keys())[0]

    @rx.event(background=True)
    async def poll_market_data(self):
        """Periodically polls the bot controller for fresh market data."""
        async with self:
            if not self.markets:
                self._initialize_mock_data()
        await asyncio.sleep(2)
        async with self:
            if "BIDEN" in self.markets:
                market = self.markets["BIDEN"]
                market["best_bid"] = (
                    round(market["best_bid"] + 0.01, 2)
                    if market["best_bid"] < 0.98
                    else 0.5
                )
                market["best_ask"] = (
                    round(market["best_ask"] + 0.01, 2)
                    if market["best_ask"] < 0.99
                    else 0.52
                )
                market["inventory"] += 10 if market["best_bid"] > 0.55 else -5
                market["unrealized_pnl"] += (market["best_bid"] - 0.5) * 10
                if self.is_bot_running and market["quoting_active"]:
                    new_trade = TradeFill(
                        timestamp="12:00:01",
                        side="buy",
                        price=market["best_bid"],
                        size=10,
                        market_id="BIDEN",
                    )
                    market["recent_trades"].insert(0, new_trade)
                    if len(market["recent_trades"]) > 10:
                        market["recent_trades"].pop()
        return BotState.poll_market_data

    @rx.event
    def start_bot(self):
        self.is_bot_running = True
        self._add_log("info", "Bot started. Initializing market data polling.")
        return BotState.poll_market_data

    @rx.event
    def stop_bot(self):
        self.is_bot_running = False
        self._add_log("warning", "Bot polling stopped.")

    def _add_log(self, level: str, message: str):
        """Adds a message to the log."""
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_messages.insert(
            0, {"level": level, "message": f"{timestamp} - {message}"}
        )
        if len(self.log_messages) > 100:
            self.log_messages.pop()

    def _initialize_mock_data(self):
        """Sets up initial mock data for demonstration."""
        self._add_log("info", "Initializing with mock market data.")
        strategy_template = {
            "target_spread_bps": 200,
            "max_inventory": 1000,
            "base_quote_size": 100,
            "skew": 0.5,
            "enabled": True,
        }
        self.markets = {
            "BIDEN": Market(
                market_id="BIDEN",
                ticker="BIDEN.WINS.2024",
                description="Will Joe Biden win the 2024 presidential election?",
                best_bid=0.5,
                best_ask=0.52,
                my_bid_price=0.49,
                my_bid_size=100,
                my_ask_price=0.53,
                my_ask_size=100,
                inventory=50,
                unrealized_pnl=25.5,
                quoting_active=True,
                strategy_params=strategy_template.copy(),
                order_book=[
                    {"side": "ask", "price": 0.53, "size": 500},
                    {"side": "ask", "price": 0.52, "size": 1200},
                    {"side": "bid", "price": 0.5, "size": 800},
                    {"side": "bid", "price": 0.49, "size": 1500},
                ],
                recent_trades=[
                    {
                        "timestamp": "11:59:30",
                        "side": "sell",
                        "price": 0.51,
                        "size": 50,
                        "market_id": "BIDEN",
                    }
                ],
            ),
            "TRUMP": Market(
                market_id="TRUMP",
                ticker="TRUMP.WINS.2024",
                description="Will Donald Trump win the 2024 presidential election?",
                best_bid=0.48,
                best_ask=0.5,
                my_bid_price=0.47,
                my_bid_size=100,
                my_ask_price=0.51,
                my_ask_size=100,
                inventory=-20,
                unrealized_pnl=-10.2,
                quoting_active=False,
                strategy_params=strategy_template.copy(),
                order_book=[
                    {"side": "ask", "price": 0.51, "size": 900},
                    {"side": "ask", "price": 0.5, "size": 1100},
                    {"side": "bid", "price": 0.48, "size": 600},
                    {"side": "bid", "price": 0.47, "size": 1300},
                ],
                recent_trades=[],
            ),
        }
        if not self.active_market_id:
            self.active_market_id = "BIDEN"
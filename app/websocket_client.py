import reflex as rx
import asyncio
import websockets
import json
import logging
from app.state import BotState


class KalshiWebsocketClient:
    def __init__(self, api_key: str, market_tickers: list[str]):
        self.api_key = api_key
        self.market_tickers = market_tickers
        self.ws_url = "wss://trading-api.kalshi.com/trade-api/ws/v2"

    async def connect(self, state_setter: BotState):
        extra_headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            async with websockets.connect(
                self.ws_url, extra_headers=extra_headers
            ) as websocket:
                async with state_setter:
                    state_setter._add_log("info", "Connected to Kalshi WebSocket.")
                if self.market_tickers:
                    subscription_msg = {
                        "id": 1,
                        "cmd": "subscribe",
                        "params": {
                            "channels": ["orderbook_delta", "ticker"],
                            "market_tickers": self.market_tickers,
                        },
                    }
                    await websocket.send(json.dumps(subscription_msg))
                while state_setter.is_bot_running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=15)
                        data = json.loads(message)
                        await self.handle_message(data, state_setter)
                    except asyncio.TimeoutError as e:
                        logging.exception(f"WebSocket timeout: {e}")
                        ping_msg = {"id": 2, "cmd": "ping"}
                        await websocket.send(json.dumps(ping_msg))
                    except websockets.exceptions.ConnectionClosed as e:
                        logging.exception(f"WebSocket connection closed: {e}")
                        async with state_setter:
                            state_setter._add_log(
                                "error", "WebSocket connection closed."
                            )
                        break
        except Exception as e:
            logging.exception(f"WebSocket connection failed: {e}")
            async with state_setter:
                state_setter._add_log("error", f"WebSocket connection failed: {e}")
                state_setter.is_bot_running = False

    async def handle_message(self, data: dict, state_setter: BotState):
        msg_type = data.get("type")
        if msg_type == "orderbook_delta":
            await self._handle_orderbook_delta(data, state_setter)
        elif msg_type == "ticker":
            await self._handle_ticker(data, state_setter)
        elif msg_type == "subscribed":
            async with state_setter:
                state_setter._add_log(
                    "info", f"Subscribed to channel: {data['msg']['channel']}"
                )

    async def _handle_orderbook_delta(self, data: dict, state_setter: BotState):
        msg = data.get("msg", {})
        market_ticker = msg.get("market_ticker")
        if not market_ticker:
            return
        async with state_setter:
            if market_ticker in state_setter.markets:
                log_msg = f"Order book update for {market_ticker}: {msg['side']} at {msg['price']} cents, size change {msg['delta']}"

    async def _handle_ticker(self, data: dict, state_setter: BotState):
        msg = data.get("msg", {})
        market_ticker = msg.get("market_ticker")
        if not market_ticker:
            return
        async with state_setter:
            if market_ticker in state_setter.markets:
                state_setter.markets[market_ticker]["best_bid"] = (
                    msg.get("yes_bid", 0) / 100.0
                )
                state_setter.markets[market_ticker]["best_ask"] = (
                    msg.get("yes_ask", 0) / 100.0
                )
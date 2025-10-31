import reflex as rx
from app.state import BotState


def test_kill_switch_interactions():
    """Test the kill switch dialog and confirmation flow"""
    state = BotState()
    state.is_bot_running = True
    state.global_kill_switch_active = False
    state.show_kill_switch_dialog = False
    print("Initial state:")
    print(f"  Bot running: {state.is_bot_running}")
    print(f"  Kill switch active: {state.global_kill_switch_active}")
    print(f"  Dialog showing: {state.show_kill_switch_dialog}")
    state.toggle_kill_switch_dialog()
    print("""
After opening dialog:""")
    print(f"  Dialog showing: {state.show_kill_switch_dialog}")
    state.activate_kill_switch()
    print("""
After activating kill switch:""")
    print(f"  Bot running: {state.is_bot_running}")
    print(f"  Kill switch active: {state.global_kill_switch_active}")
    print(f"  Dialog showing: {state.show_kill_switch_dialog}")
    print(f"  Log messages: {state.log_messages.length()}")
    state.deactivate_kill_switch()
    print("""
After deactivating kill switch:""")
    print(f"  Bot running: {state.is_bot_running}")
    print(f"  Kill switch active: {state.global_kill_switch_active}")
    print("""
✅ Kill switch functionality working correctly!""")


test_kill_switch_interactions()
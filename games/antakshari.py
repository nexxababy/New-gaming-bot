import random, asyncio
from pyrogram import filters
from utils import pretty_name
from config import DAILY_REWARD

active_antakshari = {}

def register_antakshari(app, db):
    @app.on_message(filters.command("anta"))
    async def anta_cmd(_, m):
        chat_id = m.chat.id
        if len(m.command) < 2:
            return await m.reply_text("Usage:\n/anta start | /anta join | /anta stop | /anta <word>")

        action = m.command[1].lower()

        # 🎮 Start new game
        if action == "start":
            if chat_id in active_antakshari:
                return await m.reply_text("⚠️ Game already running!")
            letter = random.choice("abcdefghijklmnopqrstuvwxyz")
            active_antakshari[chat_id] = {
                "current_letter": letter,
                "used": set(),
                "players": {},
                "turn": None,
                "time_limit": 20
            }
            return await m.reply_text(f"🎶 Antakshari started!\nJoin with /anta join\nFirst letter will be **{letter.upper()}**")

        # 👥 Join game
        if action == "join":
            if chat_id not in active_antakshari:
                return await m.reply_text("Start with /anta start")
            state = active_antakshari[chat_id]
            state["players"][m.from_user.id] = True
            return await m.reply_text(f"{pretty_name(m)} joined the game ✅")

        # ⏹ Stop game
        if action == "stop":
            if chat_id in active_antakshari:
                active_antakshari.pop(chat_id)
                return await m.reply_text("⏹ Antakshari stopped.")
            return await m.reply_text("No game running.")

        # 🎲 Player turn (word play)
        if chat_id not in active_antakshari:
            return await m.reply_text("Start with /anta start")
        state = active_antakshari[chat_id]

        word = action.lower()

        # Only allow current turn player
        if state["turn"] != m.from_user.id:
            return await m.reply_text("⏳ Wait for your turn!")

        # Word rules
        if not word.startswith(state["current_letter"]):
            await eliminate_player(chat_id, m.from_user.id, m, reason="Wrong starting letter!")
            return
        if word in state["used"]:
            await eliminate_player(chat_id, m.from_user.id, m, reason="Word already used!")
            return

        # ✅ Word accepted
        state["used"].add(word)
        state["current_letter"] = word[-1]

        await db.ensure_user(m.from_user.id, pretty_name(m))
        u = await db.get_user(m.from_user.id)
        await db.update_user(m.from_user.id, coins=u["coins"]+5, xp=u["xp"]+2)

        await m.reply_text(f"✅ {pretty_name(m)} played **{word}**!\nNext letter: {state['current_letter'].upper()}")

        # Next turn
        await next_turn(chat_id, m)

# Helper functions
async def next_turn(chat_id, m):
    state = active_antakshari[chat_id]
    players = list(state["players"].keys())
    if len(players) == 1:
        winner = players[0]
        await m.reply_text(f"🏆 Winner is {winner} 🎉\nReward: +{DAILY_REWARD} coins!")
        active_antakshari.pop(chat_id, None)
        return

    # Select next player
    state["turn"] = random.choice(players)
    state["time_limit"] = max(5, state["time_limit"]-2)

    await m.reply_text(f"🎤 Next turn: {state['turn']}\nLetter: {state['current_letter'].upper()}\nTime: {state['time_limit']}s")

    # Wait for turn
    await asyncio.sleep(state["time_limit"])
    # If player didn't play
    if state and state["turn"] == state["turn"]:  # still same turn
        await eliminate_player(chat_id, state["turn"], m, reason="⏰ Timeout!")

async def eliminate_player(chat_id, uid, m, reason):
    state = active_antakshari[chat_id]
    state["players"].pop(uid, None)
    await m.reply_text(f"❌ {uid} eliminated! {reason}")
    await next_turn(chat_id, m)

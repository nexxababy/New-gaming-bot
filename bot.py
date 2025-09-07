import asyncio
import random
import logging
import re
import json
import os
from datetime import datetime, timedelta

from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# -----------------------------
# Config
# -----------------------------
API_ID = 12345  # replace with your api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "users.json")

# -----------------------------
# Logger
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GamingBot")

# -----------------------------
# Database
# -----------------------------
db = {"users": {}, "daily": {}}

def load_db():
    global db
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                db = json.load(f)
                logger.info("Database loaded with %d users", len(db.get("users", {})))
        except Exception as e:
            logger.error("Error loading DB: %s", e)
            db = {"users": {}, "daily": {}}

def save_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

def pretty_name(name: str) -> str:
    return name.strip().title() if name else ""

async def ensure_user(uid: int, name: str):
    uid = str(uid)
    if uid not in db["users"]:
        db["users"][uid] = {"name": pretty_name(name), "coins": 0, "xp": 0}
        save_db()

async def get_user(uid: int):
    return db["users"].get(str(uid), {"name": "Unknown", "coins": 0, "xp": 0})

async def update_user(uid: int, coins: int = None, xp: int = None):
    uid = str(uid)
    if uid not in db["users"]:
        return
    if coins is not None:
        db["users"][uid]["coins"] = coins
    if xp is not None:
        db["users"][uid]["xp"] = xp
    save_db()

async def get_all_users():
    return db["users"]

# -----------------------------
# Init Bot
# -----------------------------
app = Client("gaming-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# -----------------------------
# Guess Game
# -----------------------------
active_guess = {}

@app.on_message(filters.command("guess"))
async def guess_cmd(c: Client, m: Message):
    num = random.randint(1, 10)
    active_guess[m.chat.id] = num
    await ensure_user(m.from_user.id, m.from_user.first_name)
    await m.reply_text("🤔 I picked a number (1–10). Use /try <n>")

@app.on_message(filters.command("try"))
async def try_cmd(c: Client, m: Message):
    if m.chat.id not in active_guess:
        return await m.reply_text("Start with /guess first.")
    if len(m.command) < 2:
        return await m.reply_text("Usage: /try 5")

    try:
        g = int(m.command[1])
    except ValueError:
        return await m.reply_text("Give a number 1–10.")

    target = active_guess[m.chat.id]
    if g == target:
        await ensure_user(m.from_user.id, m.from_user.first_name)
        u = await get_user(m.from_user.id)
        await update_user(m.from_user.id, coins=u["coins"] + 10, xp=u["xp"] + 3)
        active_guess.pop(m.chat.id, None)
        await m.reply_text("🎉 Correct! +10 coins, +3 XP")
    else:
        hint = "higher" if g < target else "lower"
        await m.reply_text(f"❌ Nope! Try {hint}.")

# -----------------------------
# Start / Help
# -----------------------------
@app.on_message(filters.command("start"))
async def start_handler(c: Client, m: Message):
    await ensure_user(m.from_user.id, m.from_user.first_name)
    await m.reply_text("👋 Welcome! Use /guess to start a game or /help for commands.")

@app.on_message(filters.command("help"))
async def help_handler(c: Client, m: Message):
    txt = (
        "📌 Available commands:\n\n"
        "/start - Start bot\n"
        "/help - Show help\n"
        "/guess - Start guess game\n"
        "/try <n> - Try guessing number\n"
        "/profile - Show your profile\n"
        "/top - Leaderboard\n"
        "/daily - Claim daily reward"
    )
    await m.reply_text(txt)

# -----------------------------
# Profile with Rank
# -----------------------------
@app.on_message(filters.command("profile"))
async def profile_handler(c: Client, m: Message):
    uid = str(m.from_user.id)
    users = await get_all_users()
    await ensure_user(m.from_user.id, m.from_user.first_name)

    user = users.get(uid, {"name": m.from_user.first_name, "coins": 0, "xp": 0})

    # Rank निकालना (by UID, not name)
    users_sorted = sorted(users.items(), key=lambda x: (x[1]["coins"], x[1]["xp"]), reverse=True)
    rank = "Unranked"
    for i, (user_id, u) in enumerate(users_sorted, start=1):
        if user_id == uid:
            rank = f"#{i}"
            break

    text = (
        f"👤 {user['name']}\n"
        f"💰 Coins: {user.get('coins', 0)}\n"
        f"⭐ XP: {user.get('xp', 0)}\n"
        f"🏆 Rank: {rank}"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🏆 Leaderboard", callback_data="show_top")],
            [InlineKeyboardButton("🎮 Play Again", callback_data="play_game")]
        ]
    )
    await m.reply_text(text, reply_markup=buttons)

# -----------------------------
# Leaderboard
# -----------------------------
@app.on_message(filters.command("top"))
async def top_handler(c: Client, m: Message):
    users = await get_all_users()
    if not users:
        return await m.reply_text("🏆 No players yet!")

    users_sorted = sorted(users.values(), key=lambda x: (x["coins"], x["xp"]), reverse=True)
    top10 = users_sorted[:10]

    text = "🏆 Top Players Leaderboard 🏆\n\n"
    for i, u in enumerate(top10, start=1):
        text += f"{i}. {u['name']} — 💰 {u['coins']} coins | ⭐ {u['xp']} XP\n"

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("👤 My Profile", callback_data="my_profile")],
            [InlineKeyboardButton("🎮 Play Again", callback_data="play_game")]
        ]
    )
    await m.reply_text(text, reply_markup=buttons)

# -----------------------------
# Daily Reward
# -----------------------------
@app.on_message(filters.command("daily"))
async def daily_handler(c: Client, m: Message):
    uid = str(m.from_user.id)
    await ensure_user(m.from_user.id, m.from_user.first_name)

    last_claim = db["daily"].get(uid)
    now = datetime.utcnow()

    if last_claim and now < datetime.fromisoformat(last_claim) + timedelta(hours=24):
        remaining = (datetime.fromisoformat(last_claim) + timedelta(hours=24)) - now
        return await m.reply_text(
            f"⏳ You already claimed daily reward.\nCome back in {remaining.seconds//3600}h {(remaining.seconds//60)%60}m."
        )

    # reward
    reward_coins = random.randint(10, 30)
    reward_xp = random.randint(2, 6)

    user = await get_user(uid)
    await update_user(uid, coins=user["coins"] + reward_coins, xp=user["xp"] + reward_xp)
    db["daily"][uid] = now.isoformat()
    save_db()

    await m.reply_text(f"🎁 Daily Reward Claimed!\n+{reward_coins} coins\n+{reward_xp} XP")

# -----------------------------
# Callback Queries
# -----------------------------
@app.on_callback_query()
async def callback_handler(c: Client, q):
    if q.data == "my_profile":
        uid = str(q.from_user.id)
        users = await get_all_users()
        user = users.get(uid, {"name": q.from_user.first_name, "coins": 0, "xp": 0})

        users_sorted = sorted(users.items(), key=lambda x: (x[1]["coins"], x[1]["xp"]), reverse=True)
        rank = "Unranked"
        for i, (user_id, u) in enumerate(users_sorted, start=1):
            if user_id == uid:
                rank = f"#{i}"
                break

        text = (
            f"👤 {user['name']}\n"
            f"💰 Coins: {user.get('coins', 0)}\n"
            f"⭐ XP: {user.get('xp', 0)}\n"
            f"🏆 Rank: {rank}"
        )
        await q.message.edit_text(text)

    elif q.data == "show_top":
        users = await get_all_users()
        users_sorted = sorted(users.values(), key=lambda x: (x["coins"], x["xp"]), reverse=True)
        top10 = users_sorted[:10]
        text = "🏆 Top Players Leaderboard 🏆\n\n"
        for i, u in enumerate(top10, start=1):
            text += f"{i}. {u['name']} — 💰 {u['coins']} coins | ⭐ {u['xp']} XP\n"
        await q.message.edit_text(text)

    elif q.data == "play_game":
        await q.answer("🎮 Start a new game with /guess!", show_alert=True)

# -----------------------------
# Main
# -----------------------------
async def main():
    load_db()
    await app.start()
    me = await app.get_me()
    logger.info("Bot started: @%s (%s)", me.username, me.id)
    await idle()
    await app.stop()
    save_db()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        save_db()
        logger.info("Bot stopped")

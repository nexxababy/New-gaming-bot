import asyncio
import random
import logging
from datetime import datetime, timedelta

from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database import (
    init_db,
    ensure_user,
    get_user,
    update_user,
    get_all_users,
)

API_ID =   # replace with your api_id
API_HASH = ""
BOT_TOKEN = ""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GamingBot")

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
# Daily Reward
# -----------------------------
@app.on_message(filters.command("daily"))
async def daily_handler(c: Client, m: Message):
    await ensure_user(m.from_user.id, m.from_user.first_name)
    user = await get_user(m.from_user.id)

    now = datetime.utcnow()
    if user["last_daily"] and now < user["last_daily"] + timedelta(hours=24):
        remaining = (user["last_daily"] + timedelta(hours=24)) - now
        return await m.reply_text(
            f"⏳ You already claimed daily reward.\nCome back in {remaining.seconds//3600}h {(remaining.seconds//60)%60}m."
        )

    reward_coins = random.randint(10, 30)
    reward_xp = random.randint(2, 6)

    await update_user(
        m.from_user.id,
        coins=user["coins"] + reward_coins,
        xp=user["xp"] + reward_xp,
        last_daily=now,
    )

    await m.reply_text(f"🎁 Daily Reward Claimed!\n+{reward_coins} coins\n+{reward_xp} XP")


# -----------------------------
# Profile
# -----------------------------
@app.on_message(filters.command("profile"))
async def profile_handler(c: Client, m: Message):
    await ensure_user(m.from_user.id, m.from_user.first_name)
    user = await get_user(m.from_user.id)
    users = await get_all_users()

    users_sorted = sorted(users, key=lambda x: (x["coins"], x["xp"]), reverse=True)
    rank = next((f"#{i+1}" for i, u in enumerate(users_sorted) if u["uid"] == str(m.from_user.id)), "Unranked")

    text = (
        f"👤 {user['name']}\n"
        f"💰 Coins: {user['coins']}\n"
        f"⭐ XP: {user['xp']}\n"
        f"🏆 Rank: {rank}"
    )

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🏆 Leaderboard", callback_data="show_top")]]
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

    users_sorted = sorted(users, key=lambda x: (x["coins"], x["xp"]), reverse=True)[:10]
    text = "🏆 Top Players Leaderboard 🏆\n\n"
    for i, u in enumerate(users_sorted, start=1):
        text += f"{i}. {u['name']} — 💰 {u['coins']} coins | ⭐ {u['xp']} XP\n"

    await m.reply_text(text)


# -----------------------------
# Start / Help
# -----------------------------
@app.on_message(filters.command("start"))
async def start_handler(c: Client, m: Message):
    await ensure_user(m.from_user.id, m.from_user.first_name)
    await m.reply_text("👋 Welcome! Use /guess to play, /daily to claim reward, /profile to view stats.")


@app.on_message(filters.command("help"))
async def help_handler(c: Client, m: Message):
    txt = (
        "📌 Commands:\n"
        "/start - Start bot\n"
        "/help - Show help\n"
        "/guess - Start guess game\n"
        "/try <n> - Try guessing\n"
        "/daily - Claim daily reward\n"
        "/profile - Show profile\n"
        "/top - Leaderboard"
    )
    await m.reply_text(txt)


# -----------------------------
# Main
# -----------------------------
async def main():
    await init_db()
    try:
        await app.start()
        me = await app.get_me()
        logger.info("Bot started: @%s (%s)", me.username, me.id)
        await idle()
    finally:
        await app.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")

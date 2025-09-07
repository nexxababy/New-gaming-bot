import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import idle

from utils import get_logger
from main_utils import load_games_package

# Setup logging
logger = get_logger("GamingBot")

# Database placeholder (replace with your db module/connection)
db = {
    "users": {}
}

# Pyrogram client
app = Client("gaming_bot")

# ------------------- Handlers -------------------

@app.on_message(filters.command("help") & filters.private)
async def help_handler(c: Client, m: Message):
    txt = (
        "Available commands:\n"
        "/start\n"
        "/help\n"
        "/profile\n"
        "Use game commands in groups according to game docs."
    )
    await m.reply_text(txt)

@app.on_message(filters.command("profile") & filters.private)
async def profile_handler(c: Client, m: Message):
    uid = str(m.from_user.id)
    users = db.get("users", {})
    user = users.get(uid, {"coins": 0, "xp": 0})
    await m.reply_text(
        f"{m.from_user.first_name}\n"
        f"Coins: {user.get('coins',0)}\n"
        f"XP: {user.get('xp',0)}"
    )

# ------------------- Main -------------------

async def main():
    await app.start()
    me = await app.get_me()
    logger.info("Bot started: @%s (%s)", me.username, me.id)

    # load games
    loaded = load_games_package(app, db, package="games")
    logger.info("Games loaded: %s", loaded)

    # run until cancelled
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")

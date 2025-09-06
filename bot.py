# bot.py
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config
from database import JSONDatabase
from main_utils import load_games_package

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

db = JSONDatabase(config.DB_FILE)

app = Client(
    config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workdir="."
)

@app.on_message(filters.command("start") & filters.private)
async def start_handler(c: Client, m: Message):
    await m.reply_text("Hi! Gaming bot ready. Use /help to see commands.")

@app.on_message(filters.command("help") & filters.private)
async def help_handler(c: Client, m: Message):
    txt = "Available commands:\n/start\n/help\n/profile\nUse game commands in groups according to game docs."
    await m.reply_text(txt)

@app.on_message(filters.command("profile") & filters.private)
async def profile_handler(c: Client, m: Message):
    uid = str(m.from_user.id)
    users = db.get("users", {})
    user = users.get(uid, {"coins": 0, "xp": 0})
    await m.reply_text(f"{m.from_user.first_name}\nCoins: {user.get('coins',0)}\nXP: {user.get('xp',0)}")

async def main():
    await app.start()
    me = await app.get_me()
    logger.info("Bot started: @%s (%s)", me.username, me.id)

    # load games
    loaded = load_games_package(app, db, package="games")
    logger.info("Games loaded: %s", loaded)

    # run until cancelled
    from pyrogram import idle
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

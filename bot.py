import asyncio
import logging
import os
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("NewGamingBot")

try:
    from config import API_ID, API_HASH, BOT_TOKEN, DATA_DIR
except Exception:
    raise RuntimeError("Please create config.py from example_config.py and set credentials")

from database import JSONDatabase

os.makedirs(DATA_DIR, exist_ok=True)

db = JSONDatabase(DATA_DIR)
app = Client("new_gaming_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

from games import antakshari, rps

antakshari.register(app, db)
rps.register(app, db)

if __name__ == "__main__":
    LOGGER.info("Starting bot...")
    app.run()

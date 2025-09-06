# config.py - fill the placeholders with your values
import os

# from my.telegram.org and BotFather
API_ID = int(os.environ.get("API_ID", "123456"))       # replace or set env var
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "123456:ABCDEF")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))       # your uid (optional)

# runtime settings
DB_FILE = os.environ.get("DB_FILE", "data.json")
SESSION_NAME = os.environ.get("SESSION_NAME", "gaming_bot_session")
LOG_CHAT = os.environ.get("LOG_CHAT", None)  # optional: chat id for error logs

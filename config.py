# config.py - fill the placeholders with your values
import os

# from my.telegram.org and BotFather
API_ID = int(os.environ.get("API_ID", ""))       # replace or set env var
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", ""))       # your uid (optional)

# runtime settings
DB_FILE = os.environ.get("DB_FILE", "data.json")
SESSION_NAME = os.environ.get("SESSION_NAME", "gaming_bot_session")
LOG_CHAT = osenvionge("CAT", None)  # optional: chat id for error logs

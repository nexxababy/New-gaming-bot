# config.py - fill the placeholders with your values
import os

# from my.telegram.org and BotFather
API_ID = int(os.environ.get("API_ID", "26344421"))       # replace or set env var
API_HASH = os.environ.get("API_HASH", "4bbcf08096c88dfa79c1e8e03af3ab3a")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8474933953:AAHFAqTJGkSiN7ltZUexXV7syiwdZ6YsiPg")
OWNER_ID = int(os.environ.get("OWNER_ID", "7639271205"))       # your uid (optional)

# runtime settings
DB_FILE = os.environ.get("DB_FILE", "data.json")
SESSION_NAME = os.environ.get("SESSION_NAME", "gaming_bot_session")
LOG_CHAT = os.environ.get("LOG_CHAT", None)  # optional: chat id for error logs

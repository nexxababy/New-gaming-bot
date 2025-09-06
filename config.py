import os

API_ID = int(os.environ.get("API_ID", "26344421"))
API_HASH = os.environ.get("API_HASH", "4bbcf08096c88dfa79c1e8e03af3ab3a")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8474933953:AAHFAqTJGkSiN7ltZUexXV7syiwdZ6YsiPg")

SESSION_NAME = "gaming-bot"
DB_FILE = "gaming_bot_db.json"

START_COINS = 100
DAILY_REWARD = 50
DAILY_COOLDOWN_HOURS = 20

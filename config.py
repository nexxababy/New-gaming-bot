import os

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

SESSION_NAME = "gaming-bot"
DB_FILE = "gaming_bot_db.json"

START_COINS = 100
DAILY_REWARD = 50
DAILY_COOLDOWN_HOURS = 20

from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME
from database import JSONDB
from games.guess import register_guess
from games.rps import register_rps
from games.slots import register_slots
from games.quiz import register_quiz
from games.duel import register_duel

db = JSONDB()
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_cmd(_, m):
    await db.ensure_user(m.from_user.id, m.from_user.first_name)
    await m.reply_text("🎮 Gaming Bot Ready!\n\nCommands:\n/guess, /try\n/rps <choice>\n/spin\n/quiz, /answer\n/fight (reply) <bet>, /accept, /decline")

# Register games
register_guess(app, db)
register_rps(app, db)
register_slots(app, db)
register_quiz(app, db)
register_duel(app, db)

if name == "main":
    print("✅ Gaming Bot Running...")
    app.run()

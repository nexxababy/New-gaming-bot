import random
from pyrogram import filters
from utils import pretty_name

choices = ["rock", "paper", "scissors"]

def register_rps(app, db):
    @app.on_message(filters.command("rps"))
    async def rps_cmd(_, m):
        if len(m.command) < 2:
            return await m.reply_text("Usage: /rps <rock|paper|scissors>")
        player = m.command[1].lower()
        if player not in choices:
            return await m.reply_text("Choose rock, paper, or scissors.")

        bot_choice = random.choice(choices)
        result = None
        if player == bot_choice:
            result = "🤝 It's a tie!"
        elif (player == "rock" and bot_choice == "scissors") or \
             (player == "scissors" and bot_choice == "paper") or \
             (player == "paper" and bot_choice == "rock"):
            result = "🎉 You win! +5 coins"
            await db.ensure_user(m.from_user.id, pretty_name(m))
            u = await db.get_user(m.from_user.id)
            await db.update_user(m.from_user.id, coins=u["coins"]+5, xp=u["xp"]+2)
        else:
            result = "😢 You lose!"

        await m.reply_text(f"You: {player}\nBot: {bot_choice}\n\n{result}")

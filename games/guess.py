import random
from pyrogram import filters
from utils import pretty_name

# Active guesses will be stored here per chat
active_guess = {}

def register_guess(app, db):
    @app.on_message(filters.command("guess"))
    async def guess_cmd(_, m):
        """
        Start a new guessing game (1–10).
        """
        num = random.randint(1, 10)
        active_guess[m.chat.id] = num
        await m.reply_text("🤔 I picked a number between 1–10.\nUse /try <n> to guess!")

    @app.on_message(filters.command("try"))
    async def try_cmd(_, m):
        """
        Player tries a number guess.
        """
        if m.chat.id not in active_guess:
            return await m.reply_text("⚠️ First start a game using /guess.")

        if len(m.command) < 2:
            return await m.reply_text("Usage: /try <number>\nExample: /try 5")

        # Validate number
        try:
            g = int(m.command[1])
        except ValueError:
            return await m.reply_text("❌ Please give a valid number (1–10).")

        if g < 1 or g > 10:
            return await m.reply_text("⚠️ Only numbers between 1–10 are allowed.")

        # Get the target number
        target = active_guess[m.chat.id]

        if g == target:
            # Add/update user in database
            await db.ensure_user(m.from_user.id, pretty_name(m.from_user.first_name))
            u = await db.get_user(m.from_user.id)
            await db.update_user(m.from_user.id, coins=u["coins"] + 10, xp=u["xp"] + 3)

            # Clear active guess
            active_guess.pop(m.chat.id, None)

            await m.reply_text("🎉 Correct! You won +10 coins and +3 XP.")
        else:
            hint = "higher 🔼" if g < target else "lower 🔽"
            await m.reply_text(f"❌ Nope! Try a {hint} number.")

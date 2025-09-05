import random
from pyrogram import filters
from utils import pretty_name

active_guess = {}

def register_guess(app, db):
    @app.on_message(filters.command("guess"))
    async def guess_cmd(_, m):
        num = random.randint(1, 10)
        active_guess[m.chat.id] = num
        await m.reply_text("🤔 I picked a number (1–10). Use /try <n>")

    @app.on_message(filters.command("try"))
    async def try_cmd(_, m):
        if m.chat.id not in active_guess:
            return await m.reply_text("Start with /guess first.")
        if len(m.command) < 2:
            return await m.reply_text("Usage: /try 5")

        try:
            g = int(m.command[1])
        except ValueError:
            return await m.reply_text("Give a number 1–10.")

        target = active_guess[m.chat.id]
        if g == target:
            await db.ensure_user(m.from_user.id, pretty_name(m))
            u = await db.get_user(m.from_user.id)
            await db.update_user(m.from_user.id, coins=u["coins"]+10, xp=u["xp"]+3)
            active_guess.pop(m.chat.id, None)
            await m.reply_text("🎉 Correct! +10 coins, +3 XP")
        else:
            hint = "higher" if g < target else "lower"
            await m.reply_text(f"❌ Nope! Try {hint}.")

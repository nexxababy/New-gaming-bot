import random
from pyrogram import filters
from utils import pretty_name

symbols = ["🍒", "🍋", "🍇", "🍉", "⭐", "7️⃣"]

def register_slots(app, db):
    @app.on_message(filters.command("spin"))
    async def spin_cmd(_, m):
        slot = [random.choice(symbols) for _ in range(3)]
        result = " | ".join(slot)

        await db.ensure_user(m.from_user.id, pretty_name(m))
        u = await db.get_user(m.from_user.id)

        if len(set(slot)) == 1:
            reward = 20
            await db.update_user(m.from_user.id, coins=u["coins"]+reward, xp=u["xp"]+5)
            msg = f"🎰 {result}\nJackpot! +{reward} coins"
        elif len(set(slot)) == 2:
            reward = 5
            await db.update_user(m.from_user.id, coins=u["coins"]+reward, xp=u["xp"]+2)
            msg = f"🎰 {result}\nNice! +{reward} coins"
        else:
            msg = f"🎰 {result}\nNo luck this time."

        await m.reply_text(msg)

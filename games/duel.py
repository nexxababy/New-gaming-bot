import random
from pyrogram import filters
from utils import pretty_name

duels = {}

def register_duel(app, db):
    @app.on_message(filters.command("fight"))
    async def fight_cmd(_, m):
        if not m.reply_to_message:
            return await m.reply_text("Reply to a user with /fight <bet>")
        if len(m.command) < 2:
            return await m.reply_text("Usage: /fight <bet> (reply to a user)")

        try:
            bet = int(m.command[1])
        except ValueError:
            return await m.reply_text("Bet must be a number.")

        challenger = m.from_user.id
        opponent = m.reply_to_message.from_user.id

        await db.ensure_user(challenger, pretty_name(m))
        await db.ensure_user(opponent, m.reply_to_message.from_user.first_name)

        duels[opponent] = {"challenger": challenger, "bet": bet, "chat": m.chat.id}
        await m.reply_text(f"⚔️ {m.from_user.first_name} challenges {m.reply_to_message.from_user.first_name} for {bet} coins!\nUse /accept or /decline")

    @app.on_message(filters.command("accept"))
    async def accept_cmd(_, m):
        if m.from_user.id not in duels:
            return await m.reply_text("No one challenged you.")
        duel = duels.pop(m.from_user.id)
        challenger, bet, chat_id = duel["challenger"], duel["bet"], duel["chat"]

        winner = random.choice([challenger, m.from_user.id])
        loser = challenger if winner == m.from_user.id else m.from_user.id

        u_w = await db.get_user(winner)
        u_l = await db.get_user(loser)
        await db.update_user(winner, coins=u_w["coins"]+bet, wins=u_w["wins"]+1)
        await db.update_user(loser, coins=max(0, u_l["coins"]-bet), losses=u_l["losses"]+1)

        await m.reply_text(f"🥊 Duel Result:\nWinner: {winner}\nLoser: {loser}\nBet: {bet} coins")

    @app.on_message(filters.command("decline"))
    async def decline_cmd(_, m):
        if m.from_user.id not in duels:
            return await m.reply_text("No one challenged you.")
        duels.pop(m.from_user.id)
        await m.reply_text("❌ Duel declined.")

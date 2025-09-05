import random
from pyrogram import filters
from utils import pretty_name

questions = [
    ("What is the capital of France?", "paris"),
    ("5 + 7 = ?", "12"),
    ("Who developed Python?", "guido van rossum"),
]

active_quiz = {}

def register_quiz(app, db):
    @app.on_message(filters.command("quiz"))
    async def quiz_cmd(_, m):
        q, a = random.choice(questions)
        active_quiz[m.from_user.id] = a
        await m.reply_text(f"❓ {q}\nReply with /answer <your answer>")

    @app.on_message(filters.command("answer"))
    async def answer_cmd(_, m):
        if m.from_user.id not in active_quiz:
            return await m.reply_text("Start a quiz with /quiz first.")
        if len(m.command) < 2:
            return await m.reply_text("Usage: /answer <text>")

        ans = " ".join(m.command[1:]).lower()
        correct = active_quiz.pop(m.from_user.id)

        if ans == correct:
            await db.ensure_user(m.from_user.id, pretty_name(m))
            u = await db.get_user(m.from_user.id)
            await db.update_user(m.from_user.id, coins=u["coins"]+10, xp=u["xp"]+5)
            await m.reply_text("✅ Correct! +10 coins, +5 XP")
        else:
            await m.reply_text(f"❌ Wrong! Correct answer: {correct}")

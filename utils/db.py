import sqlite3
import asyncio

class Database:
    def __init__(self, path="gaming.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, coins INTEGER, xp INTEGER)"
        )
        self.conn.commit()

    async def ensure_user(self, user_id, name):
        q = self.cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        if not q.fetchone():
            self.cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, name, 100, 0))
            self.conn.commit()

    async def get_user(self, user_id):
        q = self.cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return q.fetchone()

    async def update_user(self, user_id, coins=None, xp=None):
        user = await self.get_user(user_id)
        if not user:
            return
        _, name, c, x = user
        if coins is None:
            coins = c
        if xp is None:
            xp = x
        self.cur.execute("UPDATE users SET coins=?, xp=? WHERE id=?", (coins, xp, user_id))
        self.conn.commit()

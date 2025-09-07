"""
SQLite database for Gaming Bot
This keeps user data permanent (coins, xp, name).
"""

import aiosqlite
from utils import pretty_name

DB_FILE = "gamingbot.db"

# -------------------------
# Initialize DB
# -------------------------
async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                name TEXT,
                coins INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0
            )
        """)
        await db.commit()

# -------------------------
# User Functions
# -------------------------

async def ensure_user(uid: int, name: str):
    """
    Make sure user exists, if not then create.
    """
    uid = str(uid)
    async with aiosqlite.connect(DB_FILE) as db:
        # Check if exists
        async with db.execute("SELECT uid FROM users WHERE uid = ?", (uid,)) as cur:
            row = await cur.fetchone()
        if not row:
            await db.execute(
                "INSERT INTO users (uid, name, coins, xp) VALUES (?, ?, ?, ?)",
                (uid, pretty_name(name), 0, 0)
            )
            await db.commit()

async def get_user(uid: int) -> dict:
    """
    Return user data dict.
    """
    uid = str(uid)
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT name, coins, xp FROM users WHERE uid = ?", (uid,)) as cur:
            row = await cur.fetchone()
            if row:
                return {"name": row[0], "coins": row[1], "xp": row[2]}
    return {"name": "Unknown", "coins": 0, "xp": 0}

async def update_user(uid: int, coins: int = None, xp: int = None):
    """
    Update user coins and xp.
    """
    uid = str(uid)
    async with aiosqlite.connect(DB_FILE) as db:
        if coins is not None:
            await db.execute("UPDATE users SET coins = ? WHERE uid = ?", (coins, uid))
        if xp is not None:
            await db.execute("UPDATE users SET xp = ? WHERE uid = ?", (xp, uid))
        await db.commit()

async def get_all_users() -> list:
    """
    Return list of all users.
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT uid, name, coins, xp FROM users") as cur:
            rows = await cur.fetchall()
            return [{"uid": r[0], "name": r[1], "coins": r[2], "xp": r[3]} for r in rows]

# -------------------------
# Example Test
# -------------------------
if __name__ == "__main__":
    import asyncio
    async def test():
        await init_db()
        await ensure_user(123, "nexxa")
        print("User:", await get_user(123))
        await update_user(123, coins=50, xp=10)
        print("Updated:", await get_user(123))
        print("All users:", await get_all_users())

    asyncio.run(test())

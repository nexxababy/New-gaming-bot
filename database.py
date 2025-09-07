import aiosqlite
from utils import pretty_name
from datetime import datetime, timedelta

DB_FILE = "gamingbot.db"

# -----------------------------
# Initialize DB
# -----------------------------
async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                name TEXT,
                coins INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                last_daily TEXT
            )
        """)
        await db.commit()

# -----------------------------
# User Functions
# -----------------------------
async def ensure_user(uid: int, name: str):
    uid = str(uid)
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT uid FROM users WHERE uid = ?", (uid,)) as cur:
            row = await cur.fetchone()
        if not row:
            await db.execute(
                "INSERT INTO users (uid, name, coins, xp, last_daily) VALUES (?, ?, ?, ?, ?)",
                (uid, pretty_name(name), 0, 0, None)
            )
            await db.commit()

async def get_user(uid: int) -> dict:
    uid = str(uid)
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT name, coins, xp, last_daily FROM users WHERE uid = ?", (uid,)) as cur:
            row = await cur.fetchone()
            if row:
                last_daily = datetime.fromisoformat(row[3]) if row[3] else None
                return {"name": row[0], "coins": row[1], "xp": row[2], "last_daily": last_daily}
    return {"name": "Unknown", "coins": 0, "xp": 0, "last_daily": None}

async def update_user(uid: int, coins: int = None, xp: int = None, last_daily: datetime = None):
    uid = str(uid)
    async with aiosqlite.connect(DB_FILE) as db:
        if coins is not None:
            await db.execute("UPDATE users SET coins = ? WHERE uid = ?", (coins, uid))
        if xp is not None:
            await db.execute("UPDATE users SET xp = ? WHERE uid = ?", (xp, uid))
        if last_daily is not None:
            await db.execute("UPDATE users SET last_daily = ? WHERE uid = ?", (last_daily.isoformat(), uid))
        await db.commit()

async def get_all_users() -> list:
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT uid, name, coins, xp FROM users") as cur:
            rows = await cur.fetchall()
            return [{"uid": r[0], "name": r[1], "coins": r[2], "xp": r[3]} for r in rows]

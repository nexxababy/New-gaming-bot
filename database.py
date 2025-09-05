import json, os, asyncio
from typing import Dict, Any
from config import DB_FILE, START_COINS

class JSONDB:
    def init(self, path: str = DB_FILE):
        self.path = path
        self.lock = asyncio.Lock()
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"users": {}, "duels": {}}, f)

    async def read(self) -> Dict[str, Any]:
        async with self.lock:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)

    async def write(self, data: Dict[str, Any]):
        async with self.lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    async def ensure_user(self, uid: int, name: str):
        data = await self.read()
        if str(uid) not in data["users"]:
            data["users"][str(uid)] = {
                "name": name,
                "coins": START_COINS,
                "xp": 0,
                "wins": 0,
                "losses": 0,
                "last_daily": 0,
            }
            await self.write(data)

    async def update_user(self, uid: int, **kwargs):
        data = await self.read()
        if str(uid) in data["users"]:
            data["users"][str(uid)].update(kwargs)
            await self.write(data)

    async def get_user(self, uid: int):
        data = await self.read()
        return data["users"].get(str(uid))

import json
import os
from threading import Lock

class JSONDatabase:
    def __init__(self, data_dir: str = "storage"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self._locks = {}

    def _get_path(self, name: str):
        return os.path.join(self.data_dir, f"{name}.json")

    def _load(self, name: str):
        path = self._get_path(name)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, name: str, obj):
        path = self._get_path(name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    def get_collection(self, name: str):
        return JSONCollection(self, name)


class JSONCollection:
    def __init__(self, db: JSONDatabase, name: str):
        self.db = db
        self.name = name
        self._lock = Lock()

    def all(self):
        return self.db._load(self.name)

    def get(self, key, default=None):
        data = self.all()
        return data.get(str(key), default)

    def set(self, key, value):
        with self._lock:
            data = self.all()
            data[str(key)] = value
            self.db._save(self.name, data)

    def remove(self, key):
        with self._lock:
            data = self.all()
            data.pop(str(key), None)
            self.db._save(self.name, data)

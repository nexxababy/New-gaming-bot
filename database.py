# database.py
import json
import threading

class JSONDatabase:
    def __init__(self, path):
        self.path = path
        self.lock = threading.RLock()
        self._data = {}
        self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}
        except Exception:
            self._data = {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        with self.lock:
            return self._data.get(key, default)

    def set(self, key, value):
        with self.lock:
            self._data[key] = value
            self._save()

    def update(self, key, **kwargs):
        with self.lock:
            d = self._data.setdefault(key, {})
            d.update(kwargs)
            self._save()

    def all(self):
        with self.lock:
            return self._data

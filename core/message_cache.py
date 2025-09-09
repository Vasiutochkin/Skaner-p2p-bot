import time
import json
import os

class MessageCache:
    def __init__(self, ttl: int = 300, persist_file: str = "messages_cache.json"):
        """
        :param ttl: час життя повідомлення у кеші (секунди)
        :param persist_file: файл для збереження кешу між перезапусками
        """
        self.ttl = ttl
        self.persist_file = persist_file
        self.cache = {}

        # Завантажуємо кеш із файлу, якщо він існує
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    now = time.time()
                    # Завантажуємо тільки ті повідомлення, які ще валідні
                    self.cache = {
                        k: (v, ts) for k, (v, ts) in data.items() if now - ts < self.ttl
                    }
            except Exception:
                self.cache = {}

    def set(self, key: str, value: str):
        """Зберегти повідомлення у кеш"""
        self.cache[key] = (value, time.time())

    def get(self, key: str):
        """Отримати повідомлення з кешу, якщо воно ще валідне"""
        if key not in self.cache:
            return None
        value, ts = self.cache[key]
        if time.time() - ts > self.ttl:
            del self.cache[key]
            return None
        return value

    def save(self):
        """Зберегти кеш у файл"""
        try:
            with open(self.persist_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False)
        except Exception:
            pass

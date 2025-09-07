import json
import os

CACHE_FILE = "messages_cache.json"


def clear_cache():
    """Очищає кеш при старті бота"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


def _load_cache():
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r") as f:
        return set(json.load(f))


def _save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(cache), f)


def is_new_offer(key: str) -> bool:
    """
    Перевіряє, чи це новий запис (по ключу: advNo або advNo+ціна).
    """
    cache = _load_cache()
    if key in cache:
        return False
    cache.add(key)
    _save_cache(cache)
    return True

from core.message_cache import MessageCache
import time

def test_message_cache():
    cache = MessageCache(ttl=2)  # TTL = 2 секунди

    cache.set("order1", "Arbitrage found!")
    print("Get immediately:", cache.get("order1"))  # має показати значення

    time.sleep(3)  # чекаємо, поки TTL закінчиться
    print("Get after 3s:", cache.get("order1"))  # має бути None

    # Перевіримо збереження у файл
    cache.set("order2", "Test persist")
    cache.save()
    print("Cache saved to file.")

if __name__ == "__main__":
    test_message_cache()

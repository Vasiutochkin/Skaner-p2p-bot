from abc import ABC, abstractmethod

class BaseExchange(ABC):
    """Базовий клас для всіх біржових адаптерів."""

    @abstractmethod
    async def get_orderbook(self, symbol: str):
        """Отримати ордербук для торгової пари."""
        pass

    @abstractmethod
    async def get_trading_pairs(self):
        """Отримати список торгових пар біржі."""
        pass

    @abstractmethod
    async def get_user_balance(self):
        """Отримати баланс користувача (якщо потрібно)."""
        pass

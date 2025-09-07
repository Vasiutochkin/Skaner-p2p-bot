def calculate_spread(buy_price: float, sell_price: float) -> float:
    """Рахує спред у %"""
    return ((sell_price - buy_price) / buy_price) * 100

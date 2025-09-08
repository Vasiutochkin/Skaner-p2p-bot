from config import SPREAD_THRESHOLD

def calculate_spread(buy_price: float, sell_price: float) -> float:
    return ((sell_price - buy_price) / buy_price) * 100

def get_flag(fiat: str) -> str:
    country_code = fiat[:2]
    try:
        return "".join(chr(127397 + ord(c)) for c in country_code.upper())
    except Exception:
        return ""

def format_spread(spread: float) -> str:
    if spread >= SPREAD_THRESHOLD * 3:
        return f"🟢 <b>{spread:.2f}%</b>"
    elif spread >= SPREAD_THRESHOLD * 2:
        return f"🟡 <b>{spread:.2f}%</b>"
    else:
        return f"🔴 <b>{spread:.2f}%</b>"

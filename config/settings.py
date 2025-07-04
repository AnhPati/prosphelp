from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def get_market_offers_file(user_id: str) -> Path:
    return DATA_DIR / f"markets_{user_id}.csv"
from fastapi import APIRouter
from backend.stock import Stock

router = APIRouter()

@router.get("/stock/{symbol}")
def get_stock(symbol: str):
    stock = Stock(symbol)
    stock.set_symbol(symbol)
    stock.set_name()
    stock.set_currentPrice()
    stock.set_consensus()
    stock.set_signal()
    return {
        "symbol": stock.symbol,
        "name": stock.name,
        "current_price": stock.current_price,
        "score": stock.score,
        "consensus": stock.consensus,
        "signal": stock.signal,
    }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
import importlib
import yfinance as yf

from backend.backtesting.backtestEngine import BacktestEngine

router = APIRouter()

class BacktestRequest(BaseModel):
    ticker: str
    strategy: str
    time_period: str

STRATEGIES = {
    "mock": "backend.strategies.mockStrategy.MockStrategy",
}

TIME_PERIODS = {
    "1mo": 30,
    "6mo": 180,
    "1y": 365,
    "5y": 1825
}

@router.post("/backtest")
def run_backtest(request: BacktestRequest):
    """Run a backtest with the specified parameters"""
    
    # Validate inputs
    if request.strategy not in STRATEGIES:
        raise HTTPException(status_code=400, detail=f"Invalid strategy: {request.strategy}")
    
    if request.time_period not in TIME_PERIODS:
        raise HTTPException(status_code=400, detail=f"Invalid time period: {request.time_period}")
    
    try:
        # Load strategy dynamically
        module_path, class_name = STRATEGIES[request.strategy].rsplit(".", 1)
        module = importlib.import_module(module_path)
        StrategyClass = getattr(module, class_name)
        strategy = StrategyClass()
        
        # Fetch price data
        end_date = date.today()
        start_date = end_date - timedelta(days=TIME_PERIODS[request.time_period])
        
        df = yf.download(request.ticker, start=start_date, end=end_date, progress=False)
        if df.empty:
            raise HTTPException(status_code=400, detail=f"No price data found for ticker: {request.ticker}")
        
        # Convert dataframe to list of dicts
        price_data = []
        for idx, row in df.iterrows():
            price_data.append({
                "date": idx.date(),
                "open": float(row["Open"]),
                "close": float(row["Close"]),
                "symbol": request.ticker
            })
        
        # Run backtest
        engine = BacktestEngine(
            ticker=request.ticker,
            price_data=price_data,
            strategy=strategy
        )
        
        result = engine.run()
        
        # Convert result to dict with trades
        result_dict = result.to_dict()
        result_dict["trades"] = [trade.to_dict() for trade in result.trades]
        
        return result_dict
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest execution failed: {str(e)}")

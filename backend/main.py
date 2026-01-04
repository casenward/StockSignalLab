from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import stock_routes, backtest_routes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_routes.router, prefix="/api", tags=["Stocks"])
app.include_router(backtest_routes.router, prefix="/api", tags=["Backtest"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Analysis and Backtesting API"}
    



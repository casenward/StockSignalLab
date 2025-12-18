from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import stock_routes
import backend.calculators.signal_calculator as signal_calculator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_routes.router, prefix="/api", tags=["Stocks"])

@app.get("/")
def read_root():
    signal = signal_calculator.signal_calculator(ticker="VRT") ## Test with SMCI ticker
    return {"Signal": signal}
    



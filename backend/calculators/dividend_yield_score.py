import backend.apis.finnhub as finnhub


def get_dividend_yield_score(stock_obj) -> float:
    metrics = finnhub.get_metrics(stock_obj.symbol)["metric"]
    dividend_yield = metrics.get("dividendYield")
    if dividend_yield is None or dividend_yield < 0:
        return 50  # Neutral score if no data or invalid dividend yield
    if dividend_yield > 5:
        return 100
    elif dividend_yield > 4:
        return 80
    elif dividend_yield > 3:
        return 60
    elif dividend_yield > 2:
        return 40
    elif dividend_yield > 1:
        return 20
    else:
        return 0

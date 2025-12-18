import backend.apis.finnhub as finnhub


def get_pb_ratio_score(stock_obj) -> float:
    current_price = stock_obj.current_price     # Ensure current price is set
    if current_price is None:
        stock_obj.set_currentPrice()
        current_price = stock_obj.current_price
    metrics = finnhub.get_metrics(stock_obj.symbol)["metric"]
    bvps = metrics.get("bookValuePerShareAnnual")
    if bvps is None or bvps == 0:
        return 50  # Neutral score if no data or invalid book value
    pb_ratio = current_price / bvps
    if pb_ratio < 1:
        return 100
    elif pb_ratio < 2:
        return 80
    elif pb_ratio < 3:                    # Scoring can be adjusted based on testing and analysis
        return 60
    elif pb_ratio < 4:
        return 40
    elif pb_ratio < 5:
        return 20
    else:
        return 0

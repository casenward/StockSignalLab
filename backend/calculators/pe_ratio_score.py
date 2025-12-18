import backend.apis.finnhub as finnhub


def get_pe_ratio_score(stock_obj) -> float:
    metrics = finnhub.get_metrics(stock_obj.symbol)["metric"]
    pe_ratio = metrics.get("peBasicExclExtraTTM")
    if pe_ratio is None or pe_ratio <= 0:
        return 50  # Neutral score if no data or invalid PE ratio
    if pe_ratio < 10:
        return 100
    elif pe_ratio < 15:
        return 80
    elif pe_ratio < 20:                    # Scoring can be adjusted based on testing and analysis
        return 60
    elif pe_ratio < 25:
        return 40
    elif pe_ratio < 30:
        return 20
    else:
        return 0

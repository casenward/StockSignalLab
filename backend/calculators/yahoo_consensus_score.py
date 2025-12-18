import backend.apis.yahoo as yahoo


def get_yahoo_consensus_score(symbol: str) -> float:
    return yahoo.getYahoo_consensus(symbol)[1]

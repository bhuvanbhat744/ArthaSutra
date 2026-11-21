
import re

KNOWN_TOKENS = {
    "BTC": ["bitcoin", "btc"],
    "ETH": ["ethereum", "ether", "eth"],
    "BNB": ["binance coin", "bnb"],
    "SOL": ["solana", "sol"],
    "XRP": ["ripple", "xrp"],
    "ADA": ["cardano", "ada"],
    "DOGE": ["dogecoin", "doge"],
    "AVAX": ["avalanche", "avax"],
    "MATIC": ["polygon", "matic"],
    "AAVE": ["aave"],
    "AERO": ["aerodrome", "aero"],
    "USDC": ["usd coin", "usdc"]
}


def extract_tokens(article):

    tokens = []
    text = (
        (article.get("title") or "") + " " +
        (article.get("description") or "")
    ).lower()

    for symbol, keywords in KNOWN_TOKENS.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                tokens.append(symbol)
                break

    article["tokens"] = sorted(set(tokens))

    return article

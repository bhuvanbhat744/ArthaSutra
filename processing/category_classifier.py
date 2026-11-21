
import re


CATEGORY_KEYWORDS = {
    "Finance": [
        "funding", "investment", "investor", "valuation",
        "ipo", "revenue", "profit", "financial", "capital",
        "bank", "billion", "million", "treasury"
    ],

    "Government & Policy": [
        "government", "regulation", "regulatory", "sec",
        "law", "policy", "ban", "legislation", "court",
        "legal", "tax", "central bank", "congress"
    ],

    "Technology": [
        "technology", "artificial intelligence", "ai",
        "innovation", "software", "hardware", "developer",
        "machine learning", "cryptography", "research"
    ],

    "Security": [
        "hack", "hacked", "exploit", "security",
        "vulnerability", "attack", "stolen", "breach",
        "scam", "phishing"
    ],

    "Markets & Trading": [
        "price", "trading", "market", "bullish", "bearish",
        "surge", "crash", "rally", "selloff", "volume",
        "liquidation", "volatility", "technical analysis"
    ],

    "DeFi": [
        "defi", "decentralized finance", "lending",
        "borrowing", "yield farming", "staking",
        "liquidity pool", "dex", "protocol"
    ],

    "Business & Partnerships": [
        "partnership", "collaboration", "acquisition",
        "merger", "deal", "integration", "company",
        "business", "launches partnership"
    ],

    "Adoption & Payments": [
        "adoption", "payment", "payments", "merchant",
        "accepts bitcoin", "mass adoption",
        "real-world use", "transaction"
    ],

    "Blockchain Infrastructure": [
        "blockchain", "mainnet", "testnet", "layer 1",
        "layer 2", "scaling", "network upgrade",
        "consensus", "validator", "interoperability"
    ],

    "Exchanges & Listings": [
        "exchange", "listed", "listing", "delisting",
        "binance", "coinbase", "kraken", "trading pair"
    ],

    "NFTs & Gaming": [
        "nft", "non-fungible", "gaming", "gamefi",
        "metaverse", "digital collectibles"
    ],

    "Stablecoins": [
        "stablecoin", "stablecoins", "usdt", "usdc",
        "tether", "depegged", "peg"
    ],

    "Mining & Energy": [
        "mining", "miner", "miners", "hashrate",
        "proof of work", "energy consumption",
        "renewable energy"
    ]
}


def classify_category(article):

    text = (
        (article.get("title") or "") + " " +
        (article.get("description") or "")
    ).lower()

    category_scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                score += 1

        if score > 0:
            category_scores[category] = score

    if category_scores:
        category = max(category_scores, key=category_scores.get)
    else:
        category = "General"

    article["news_category"] = category

    return article

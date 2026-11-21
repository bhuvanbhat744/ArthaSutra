EVENT_KEYWORDS = {
    "REGULATION": ["regulation", "sec", "government", "ban", "law"],
    "PARTNERSHIP": ["partnership", "collaboration", "integrate"],
    "PRICE_MOVEMENT": ["price", "surge", "crash", "rally", "跌"],
    "SECURITY": ["hack", "exploit", "attack", "vulnerability"],
    "ADOPTION": ["adoption", "launch", "payment", "accept"],
    "UPGRADE": ["upgrade", "update", "mainnet", "protocol"]
}


def classify_event(article):
    text = (
        (article.get("title") or "") + " " +
        (article.get("description") or "")
    ).lower()

    category = "GENERAL"

    for event, keywords in EVENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            category = event
            break

    article["event_category"] = category

    return article
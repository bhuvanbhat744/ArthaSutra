def generate_insight(article):
    matched_tokens = article.get("matched_tokens", [])
    event_category = article.get("event_category", "GENERAL")

    if not matched_tokens:
        return "No direct connection to your portfolio was found."

    tokens = ", ".join(matched_tokens)

    return (
        f"This article is relevant to your portfolio because "
        f"it mentions {tokens}. The reported event is categorized "
        f"as {event_category}. You may want to follow how this "
        f"development affects these assets."
    )
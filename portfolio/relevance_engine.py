from database.db import get_connection


def get_relevant_news():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT token_symbol FROM portfolio")
    portfolio_tokens = {
        row[0].upper() for row in cursor.fetchall()
    }

    cursor.execute("""
        SELECT title, description, url, source,
               published_at, tokens, event_category, news_category
        FROM news_articles
    """)

    articles = cursor.fetchall()
    connection.close()

    relevant_articles = []

    for article in articles:
        tokens = article[5] or ""

        article_tokens = {
            token.strip().upper()
            for token in tokens.split(",")
            if token.strip()
        }

        matched_tokens = portfolio_tokens.intersection(article_tokens)

        if matched_tokens:
            relevant_articles.append({
                "title": article[0],
                "description": article[1],
                "url": article[2],
                "source": article[3],
                "published_at": article[4],
                "tokens": list(article_tokens),
                "event_category": article[6],
                "news_category": article[7] or "General",
                "matched_tokens": list(matched_tokens)
            })

    return relevant_articles
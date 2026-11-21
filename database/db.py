import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "crypto_news.db"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT UNIQUE,
            source TEXT,
            published_at TEXT,
            tokens TEXT,
            event_category TEXT,
            news_category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_symbol TEXT NOT NULL UNIQUE,
            quantity REAL
        )
    """)

    # Add the new column to existing databases if it is missing
    cursor.execute("PRAGMA table_info(news_articles)")
    columns = [row[1] for row in cursor.fetchall()]

    if "news_category" not in columns:
        cursor.execute(
            "ALTER TABLE news_articles ADD COLUMN news_category TEXT"
        )

    connection.commit()
    connection.close()


def save_news_articles(articles):
    connection = get_connection()
    cursor = connection.cursor()

    for article in articles:
        tokens = article.get("tokens") or []
        tokens = ", ".join(tokens)

        cursor.execute("""
            INSERT INTO news_articles
            (title, description, url, source, published_at,
             tokens, event_category, news_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                description = excluded.description,
                source = excluded.source,
                published_at = excluded.published_at,
                tokens = excluded.tokens,
                event_category = excluded.event_category,
                news_category = excluded.news_category
        """, (
            article.get("title"),
            article.get("description"),
            article.get("link"),
            article.get("source_name"),
            article.get("pubDate"),
            tokens,
            article.get("event_category"),
            article.get("news_category")
        ))

    connection.commit()
    connection.close()
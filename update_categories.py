from database.db import get_connection
from processing.category_classifier import classify_category

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, title, description
    FROM news_articles
""")

articles = cursor.fetchall()

updated = 0

for article in articles:
    article_id, title, description = article

    data = {
        "title": title,
        "description": description
    }

    data = classify_category(data)

    cursor.execute("""
        UPDATE news_articles
        SET news_category = ?
        WHERE id = ?
    """, (data["news_category"], article_id))

    updated += 1

connection.commit()
connection.close()

print(f"Successfully updated {updated} articles!")
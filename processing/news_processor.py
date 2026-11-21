
from processing.cleaner import clean_article
from processing.token_extractor import extract_tokens
from processing.event_classifier import classify_event
from processing.category_classifier import classify_category
from processing.deduplicator import remove_duplicates


def process_news(articles):
    processed_articles = []

    for article in articles:
        article = clean_article(article)
        article = extract_tokens(article)
        article = classify_event(article)
        article = classify_category(article)

        processed_articles.append(article)

    processed_articles = remove_duplicates(processed_articles)

    return processed_articles

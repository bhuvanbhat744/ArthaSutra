def remove_duplicates(articles):
    unique_articles = []
    seen_urls = set()
    seen_titles = set()

    for article in articles:
        url = article.get("link") or article.get("url")
        title = (article.get("title") or "").strip().lower()

        if url:
            if url in seen_urls:
                continue
            seen_urls.add(url)

        elif title:
            if title in seen_titles:
                continue
            seen_titles.add(title)

        unique_articles.append(article)

    return unique_articles
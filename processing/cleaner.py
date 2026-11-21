def clean_article(article):
    title = article.get("title") or ""
    description = article.get("description") or ""

    title = " ".join(title.split())
    description = " ".join(description.split())

    article["title"] = title
    article["description"] = description

    return article
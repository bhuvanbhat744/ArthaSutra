import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWSDATA_API_KEY")

API_URL = "https://newsdata.io/api/1/crypto"

def fetch_news():
    if not API_KEY:
        raise ValueError("NewsData API key not found in .env")

    headers = {
        "X-ACCESS-KEY": API_KEY
    }

    params = {
        "domainurl": "coindesk.com,cointelegraph.com,decrypt.co/news,theblock.co,news.bitcoin.com",
        "language": "en",
        "size": 10
    }

    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    
    response.raise_for_status()

    data = response.json()

    return data


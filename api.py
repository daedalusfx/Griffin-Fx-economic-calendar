from fastapi import FastAPI
from typing import List, Dict, Any

# ساخت یک نمونه از FastAPI
app = FastAPI(
    title="Economic News API",
    description="A simple API to serve scraped news from Forex Factory.",
    version="1.0.0"
)

# یک متغیر برای نگهداری داده‌های اخبار که توسط اسکرپر پر می‌شود
# این متغیر بین ماژول‌ها به اشتراک گذاشته نمی‌شود، بلکه توسط main.py مدیریت می‌شود
news_storage: List[Dict[str, Any]] = []

@app.get("/api/news", 
         summary="Get Upcoming Economic Events",
         response_description="A list of economic events")
async def get_news():
    """
    این endpoint لیستی از اخبار اقتصادی ذخیره شده را برمی‌گرداند.
    """
    return {"events": news_storage}

def update_news_data(data: List[Dict[str, Any]]):
    """
    یک تابع کمکی که توسط اسکریپت اصلی برای به‌روزرسانی داده‌ها فراخوانی می‌شود.
    """
    global news_storage
    print(f"Updating news data with {len(data)} items.")
    news_storage = data
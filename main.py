import uvicorn # type: ignore
import time
import threading
from scraper import fetch_and_parse_calendar
from api import app, update_news_data

# زمان به‌روزرسانی داده‌ها (به ثانیه)، مثلا هر ۶ ساعت
REFRESH_INTERVAL = 6 * 60 * 60 # 21600 ثانیه

def schedule_scraper():
    """
    یک حلقه بی‌نهایت که اسکرپر را در فواصل زمانی مشخص اجرا می‌کند.
    """
    while True:
        print("Running scraper...")
        # داده‌های جدید را از سایت استخراج کن
        fresh_data = fetch_and_parse_calendar()
        
        # داده‌های سرور API را با اطلاعات جدید به‌روز کن
        update_news_data(fresh_data)
        
        print(f"Scraping complete. Next run in {REFRESH_INTERVAL / 3600} hours.")
        # تا نوبت بعدی صبر کن
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    # --- اجرای اولیه اسکرپر ---
    # در ابتدای کار، یک بار داده‌ها را می‌گیریم تا API از ابتدا خالی نباشد
    print("Performing initial data scrape...")
    initial_data = fetch_and_parse_calendar()
    update_news_data(initial_data)
    
    # --- راه‌اندازی زمان‌بندی در یک ترد (Thread) جداگانه ---
    # این کار باعث می‌شود حلقه زمان‌بندی، اجرای سرور را مسدود نکند
    scheduler_thread = threading.Thread(target=schedule_scraper, daemon=True)
    scheduler_thread.start()
    
    # --- راه‌اندازی سرور FastAPI ---
    # سرور روی آدرس محلی و پورت ۸۰۰۰ اجرا می‌شود
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
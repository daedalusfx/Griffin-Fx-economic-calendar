# import requests
# from bs4 import BeautifulSoup
# import datetime

# # هدرها برای شبیه‌سازی یک مرورگر واقعی
# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# def parse_forex_factory_html(html_content):
#     """
#     محتوای HTML دانلود شده از Forex Factory را تحلیل و داده‌های تقویم را استخراج می‌کند.
#     """
#     news_data = []
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     # پیدا کردن تمام ردیف‌های جدول تقویم
#     table_rows = soup.select("tr.calendar__row")
    
#     current_date_str = ""

#     for row in table_rows:
#         # --- گام ۱: استخراج و مدیریت تاریخ ---
#         date_cell = row.select_one("td.calendar__cell--date")
#         if date_cell:
#             # تمیز کردن متن تاریخ و حذف روز هفته
#             # مثال ورودی: 'Thu <span>Jul 31</span>' -> خروجی: 'Jul 31'
#             date_text_content = date_cell.get_text(separator=' ', strip=True)
#             parts = date_text_content.split(' ')
#             if len(parts) > 1:
#                 current_date_str = f"{parts[1]} {parts[2]}"

#         # استخراج سایر اطلاعات
#         time_cell = row.select_one("td.calendar__time")
#         currency_cell = row.select_one("td.calendar__currency")
#         impact_cell = row.select_one("td.calendar__impact span") # مستقیم به تگ span می‌رویم
#         event_cell = row.select_one("td.calendar__event")
        
#         # فقط ردیف‌هایی که تمام اطلاعات اصلی را دارند، پردازش می‌کنیم
#         if not (time_cell and currency_cell and impact_cell and event_cell):
#             continue
            
#         time_str = time_cell.text.strip()
#         currency = currency_cell.text.strip()
#         event_name = event_cell.text.strip()
        
#         # --- گام ۲: استخراج دقیق اهمیت خبر ---
#         impact_title = impact_cell.get('title', 'No Impact') # با اطمینان از title می‌خوانیم
        
#         news_item = {
#             "date": current_date_str,
#             "time": time_str,
#             "currency": currency,
#             "impact": impact_title,
#             "event": event_name,
#         }
#         news_data.append(news_item)
            
#     return news_data

# # تابع اصلی برای اجرا
# def fetch_and_parse_calendar():
#     """
#     یک تابع کامل که هم صفحه را دانلود و هم آن را تحلیل می‌کند.
#     """
#     url = "https://www.forexfactory.com/calendar"
#     try:
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()
#         return parse_forex_factory_html(response.content)
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data: {e}")
#         return []

# # برای تست مستقیم فایل
# if __name__ == "__main__":
#     # برای تست با فایل HTML دانلود شده
#     with open("Calendar _ Forex Factory.html", "rb") as f:
#         html_content = f.read()
    
#     news = parse_forex_factory_html(html_content)
#     if news:
#         print(f"Successfully extracted {len(news)} events.")
#         for item in news:
#             print(item)
#     else:
#         print("No events extracted.")
import requests
from bs4 import BeautifulSoup
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def parse_forex_factory_html(html_content):
    """
    محتوای HTML را تحلیل کرده و داده‌های تقویم را فقط برای روز جاری استخراج می‌کند.
    """
    news_data = []
    soup = BeautifulSoup(html_content, 'html.parser')
    
    today = datetime.date.today()
    # فرمت تاریخ را برای مقایسه می‌سازیم (مثال: Jul 31)
    today_str = today.strftime("%b %d").replace(" 0", " ")

    table_rows = soup.select("tr.calendar__row")
    
    current_date_str = ""

    for row in table_rows:
        # (اصلاح شده) سلکتور صحیح برای پیدا کردن سلول تاریخ
        date_cell = row.select_one("td.calendar__date")
        if date_cell:
            # وقتی سلول تاریخ پیدا می‌شود، یعنی روز جدیدی شروع شده است
            date_text_content = date_cell.get_text(separator=' ', strip=True)
            parts = date_text_content.split(' ')
            if len(parts) > 1:
                current_date_str = f"{parts[1]} {parts[2]}"

        # فقط در صورتی ادامه می‌دهیم که تاریخ استخراج شده با تاریخ امروز برابر باشد
        if current_date_str != today_str:
            continue

        # استخراج بقیه اطلاعات رویداد
        time_cell = row.select_one("td.calendar__time")
        currency_cell = row.select_one("td.calendar__currency")
        impact_cell = row.select_one("td.calendar__impact span")
        event_cell = row.select_one("td.calendar__event")
        
        if not (time_cell and currency_cell and impact_cell and event_cell):
            continue
            
        news_item = {
            "date": current_date_str,
            "time": time_cell.text.strip(),
            "currency": currency_cell.text.strip(),
            "impact": impact_cell.get('title', 'No Impact'),
            "event": event_cell.text.strip(),
        }
        news_data.append(news_item)
            
    return news_data

def fetch_and_parse_calendar():
    """
    تابع اصلی که به سایت متصل شده و داده‌های روز جاری را برمی‌گرداند.
    """
    url = "https://www.forexfactory.com/calendar"
    print("Fetching live data from Forex Factory...")
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return parse_forex_factory_html(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
import requests
from bs4 import BeautifulSoup
import json

def run():
    url = "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # استخدام BeautifulSoup لتحليل الـ HTML الذي أرسلته أنت
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استهداف الجدول بناءً على الكلاس الموجود في الكود الذي أرفقته
        table = soup.find('table', {'class': 'table table-striped table-bordered'})
        
        data = []
        if table:
            # استخراج الصفوف من الـ tbody
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    data.append({
                        "symbol": cols[0].get_text(strip=True),
                        "name": cols[1].get_text(strip=True),
                        "total_issued": cols[2].get_text(strip=True),
                        "loaned_quantity": cols[3].get_text(strip=True),
                        "loan_ratio": cols[4].get_text(strip=True)
                    })
        
        # حفظ البيانات
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ نجاح! تم استخراج {len(data)} شركة.")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run()

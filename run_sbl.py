import requests
from bs4 import BeautifulSoup
import json

def run():
    # الرابط المستهدف
    url = "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html"
    
    # تعريف المتصفح لمحاكاة الطلب كإنسان
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    
    try:
        # جلب الصفحة
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # تحليل الصفحة
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # البحث عن الجدول
        table = soup.find('table')
        if not table:
            print("لم يتم العثور على الجدول في صفحة الـ HTML")
            return

        # استخراج البيانات
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]: # تخطي صف العناوين
            cols = row.find_all('td')
            if len(cols) >= 5:
                data.append({
                    "symbol": cols[0].text.strip(),
                    "name": cols[1].text.strip(),
                    "total_issued": cols[2].text.strip(),
                    "loaned_quantity": cols[3].text.strip(),
                    "loan_ratio": cols[4].text.strip()
                })
        
        # حفظ النتائج
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ تم سحب {len(data)} صف وحفظ البيانات في data.json")

    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    run()

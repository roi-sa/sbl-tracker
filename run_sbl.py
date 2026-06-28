import requests
from bs4 import BeautifulSoup
import json
import time

def run():
    url = "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html"
    
    # محاكاة متصفح حقيقي بالكامل
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.saudiexchange.sa/",
        "Accept-Language": "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        # إضافة تأخير بسيط لمحاكاة التصفح البشري
        time.sleep(2)
        
        response = requests.get(url, headers=headers, timeout=30)
        
        # إذا نجح الطلب، سنحلل البيانات
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'table table-striped table-bordered'})
            
            data = []
            if table:
                rows = table.find('tbody').find_all('tr')
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
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ تم سحب {len(data)} شركة.")
        else:
            print(f"❌ الموقع رفض الطلب بـ status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run()

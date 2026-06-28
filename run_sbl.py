import cloudscraper
from bs4 import BeautifulSoup
import json

def run():
    # استخدام cloudscraper لتجاوز حماية الـ Bot
    scraper = cloudscraper.create_scraper()
    url = "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html"
    
    try:
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج الجدول
        table = soup.find('table', {'class': 'table table-striped'})
        
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
        print(f"✅ تم سحب {len(data)} شركة بنجاح.")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run()

from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        # استخدام Firefox بدلاً من Chromium لتجاوز حظر البوتات
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        )
        page = context.new_page()
        
        url = "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html"
        
        # محاولة تحميل الصفحة
        page.goto(url, wait_until="domcontentloaded")
        
        # بدلاً من الانتظار المعقد، ننتظر فقط ظهور أي نص في الصفحة
        page.wait_for_timeout(10000)
        
        # استخراج البيانات مباشرة
        data = page.evaluate('''() => {
            const table = document.querySelector('table');
            if (!table) return [];
            const rows = Array.from(table.querySelectorAll('tr'));
            return rows.slice(1).map(row => {
                const cols = Array.from(row.querySelectorAll('td')).map(td => td.innerText.trim());
                return { 
                    "symbol": cols[0], 
                    "name": cols[1], 
                    "total_issued": cols[2], 
                    "loaned_quantity": cols[3], 
                    "loan_ratio": cols[4] 
                };
            }).filter(item => item.symbol);
        }''')
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        browser.close()

if __name__ == "__main__":
    run()

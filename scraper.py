from playwright.sync_api import sync_playwright
import json

def run():
    print("--- يبدأ السكربت الآن ---")
    with sync_playwright() as p:
        # إجبار المتصفح على وضع headless=True هنا مباشرة
        browser = p.chromium.launch(headless=True)
        print("--- تم إطلاق المتصفح بنجاح ---")
        
        context = browser.new_context()
        page = context.new_page()
        
        url = "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html"
        page.goto(url, wait_until="networkidle")
        
        data = page.evaluate('''() => {
            const table = document.querySelector('table');
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
            });
        }''')
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        browser.close()
        print("✅ انتهى السكربت بنجاح.")

if __name__ == "__main__":
    run()

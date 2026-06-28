from playwright.sync_api import sync_playwright
import json

def run():
    print("--- يبدأ العمل ---")
    with sync_playwright() as p:
        # تأكدنا أنها True ولن يغيرها شيء
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html", wait_until="networkidle")
        page.wait_for_timeout(5000)
        
        data = page.evaluate('''() => {
            const table = document.querySelector('table');
            const rows = Array.from(table.querySelectorAll('tr'));
            return rows.slice(1).map(row => {
                const cols = Array.from(row.querySelectorAll('td')).map(td => td.innerText.trim());
                return { "symbol": cols[0], "name": cols[1], "total_issued": cols[2], "loaned_quantity": cols[3], "loan_ratio": cols[4] };
            });
        }''')
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        browser.close()
        print("✅ تم بنجاح")

if __name__ == "__main__":
    run()

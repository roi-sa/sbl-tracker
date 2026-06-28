from playwright.sync_api import sync_playwright
import json
import time
import os

def run():
    print("--- يبدأ العمل ---")
    # طباعة المسار الحالي للتأكد من مكان التنفيذ
    print(f"المجلد الحالي: {os.getcwd()}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print("جاري الدخول إلى رابط الموقع...")
        page.goto("https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html", wait_until="networkidle")
        
        time.sleep(5)
        
        print("جاري انتظار تحميل الجدول...")
        try:
            page.wait_for_selector('table', timeout=30000)
            print("تم العثور على الجدول، جاري استخراج البيانات...")
        except Exception as e:
            print(f"خطأ: لم يتم العثور على الجدول. التفاصيل: {e}")
            browser.close()
            return

        data = page.evaluate('''() => {
            const table = document.querySelector('table');
            if (!table) return null;
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
        
        if data:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ تمت العملية بنجاح. تم استخراج {len(data)} سجل.")
            print(f"الملفات في المجلد الحالي: {os.listdir('.')}")
        else:
            print("❌ لم يتم استخراج أي بيانات.")
            
        browser.close()

if __name__ == "__main__":
    run()

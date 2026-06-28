from playwright.sync_api import sync_playwright
import json
import time

def run():
    print("--- يبدأ العمل ---")
    with sync_playwright() as p:
        # إعداد المتصفح بدون واجهة رسومية ليعمل على سيرفر GitHub
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # التوجه لرابط التقرير
        print("جاري الدخول إلى رابط الموقع...")
        page.goto("https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html", wait_until="networkidle")
        
        # إضافة تأخير إضافي لضمان تحميل محتويات JavaScript
        time.sleep(5)
        
        # الانتظار حتى ظهور الجدول في الصفحة
        print("جاري انتظار تحميل الجدول...")
        try:
            page.wait_for_selector('table', timeout=30000)
            print("تم العثور على الجدول، جاري استخراج البيانات...")
        except Exception as e:
            print(f"خطأ: لم يتم العثور على الجدول. التفاصيل: {e}")
            browser.close()
            return

        # استخراج البيانات من الجدول
        data = page.evaluate('''() => {
            const table = document.querySelector('table');
            if (!table) return [];
            
            // اختيار جميع الصفوف وتجاهل صف العنوان (أول صف)
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
        
        # حفظ البيانات في ملف JSON
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ تمت العملية بنجاح. تم استخراج {len(data)} سجل.")
        browser.close()

if __name__ == "__main__":
    run()

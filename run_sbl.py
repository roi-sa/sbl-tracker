from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        # فتح متصفح كروم
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # الانتقال لصفحة تداول
        page.goto("https://www.saudiexchange.sa/wps/portal/saudiexchange/hiddenwebservices/display-sbl-report")
        
        # استخراج النص من الصفحة
        content = page.content()
        
        # حفظ المحتوى للتحقق مما إذا كان الموقع يظهر بيانات أم لا
        with open("data.json", "w", encoding="utf-8") as f:
            f.write(content)
            
        browser.close()

if __name__ == "__main__":
    run()

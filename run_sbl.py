name: Run SBL Script
on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'from playwright.sync_api import sync_playwright
import json

def run():
    with sync_playwright() as p:
        # تشغيل المتصفح مع إعدادات تخفي
        browser = p.chromium.launch(headless=True)
        # تحديد User-Agent لمتصفح كروم حقيقي
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # زيارة الموقع
            page.goto("https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html", wait_until="networkidle", timeout=60000)
            
            # الانتظار حتى ظهور الجدول
            page.wait_for_selector("table", timeout=30000)
            
            # استخراج محتوى الصفحة
            html_content = page.content()
            
            # (هنا يمكنك إضافة كود BeautifulSoup لتحليل html_content)
            # لحفظ الملف مؤقتاً للتأكد من نجاح الوصول:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(html_content)
                
            print("✅ تم الوصول للصفحة بنجاح.")
            
        except Exception as e:
            print(f"❌ فشل الوصول: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install cloudscraper beautifulsoup4
      - name: Run script
        run: python run_sbl.py
      - name: Commit and push
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add data.json
          git commit -m "Update SBL data" || echo "No changes to commit"
          git push

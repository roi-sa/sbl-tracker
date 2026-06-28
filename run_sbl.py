import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

async def run():
    async with async_playwright() as p:
        # تشغيل متصفح كروم حقيقي
        browser = await p.chromium.launch(headless=True)
        # تعريف سياق يشبه متصفح مستخدم حقيقي
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # الانتقال للصفحة
        await page.goto("https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html", timeout=60000)
        
        # انتظار تحميل الجدول تحديداً
        await page.wait_for_selector("table.table-striped")
        
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # استخراج البيانات
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
        
        await browser.close()
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(run())

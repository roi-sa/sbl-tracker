import requests
import json

def run():
    # هذا الرابط هو المصدر الفعلي للبيانات (JSON API)
    url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/hiddenwebservices/display-sbl-report"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://www.saudiexchange.sa/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # تحويل البيانات إلى تنسيق JSON
        data = response.json()
        
        # استخراج القائمة المحددة من البيانات
        final_data = []
        if 'sblReportList' in data:
            for item in data['sblReportList']:
                final_data.append({
                    "symbol": item.get('symbol', ''),
                    "name": item.get('securityName', ''),
                    "total_issued": item.get('totalIssuedShares', ''),
                    "loaned_quantity": item.get('loanedQuantity', ''),
                    "loan_ratio": item.get('loanRatio', '')
                })
        
        # حفظ الملف
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ تم سحب {len(final_data)} صف بنجاح.")

    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    run()

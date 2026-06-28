import requests
import json

def run():
    # هذا الرابط هو المصدر الحقيقي الذي يغذي الجدول بالبيانات
    url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/hiddenwebservices/display-sbl-report"
    
    # تعريفات تجعل الطلب يبدو وكأنه من متصفح كروم حقيقي على ويندوز
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://www.saudiexchange.sa/Resources/Reports-v2/SBLReport_ar.html",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # استخراج البيانات ومعالجتها
        if 'sblReportList' in data:
            final_data = []
            for item in data['sblReportList']:
                final_data.append({
                    "symbol": item.get('symbol', ''),
                    "name": item.get('securityName', ''),
                    "total_issued": item.get('totalIssuedShares', ''),
                    "loaned_quantity": item.get('loanedQuantity', ''),
                    "loan_ratio": item.get('loanRatio', '')
                })
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=4)
            print(f"✅ تم سحب {len(final_data)} صف بنجاح.")
        else:
            print("⚠️ تم الوصول للسيرفر ولكن لم نجد بيانات في sblReportList.")
            
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run()

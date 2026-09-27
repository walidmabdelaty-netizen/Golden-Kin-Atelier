#!/bin/bash
echo -e "\033[1;36m=== تشغيل منصة Verdix Black Platform ===\033[0m"

# إغلاق أي عمليات سابقة عالقة على نفس المنفذ
pkill -f "api/gateway.py" 2>/dev/null

# تشغيل بوابة الواجهات في الخلفية
nohup python3 api/gateway.py > logs/api_gateway.log 2>&1 &

sleep 2
echo -e "\033[1;32m[✔] تم استعادة النظام بنجاح. الواجهات تعمل الآن في الخلفية!\033[0m"
echo -e "\033[1;33mلمراقبة السيرفر: tail -f logs/api_gateway.log\033[0m"

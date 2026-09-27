#!/bin/bash
pkill -f "core/daemon_unified.py" 2>/dev/null
pkill -f "api/gateway.py" 2>/dev/null
sleep 1

# تشغيل خادم النواة الموحد على المنفذ 7001
nohup python3 core/daemon_unified.py > logs/unified_core.log 2>&1 &
sleep 1

echo -e "\033[1;35m=====================================================\033[0m"
echo -e "\033[1;36m    VERDIX-W :: SOVEREIGN QUANTUM ENGINE [PORT: 7001] \033[0m"
echo -e "\033[1;35m=====================================================\033[0m"
echo -e "\033[1;32m [✔ شغال] Verdix-Core (سيرفر 1: تشغيل النواة والمحرك الأساسي) \033[0m"
echo -e "\033[1;32m [✔ شغال] Verdix-Quantum (سيرفر 2: بوابة السجلات المشفرة) \033[0m"
echo -e "\033[1;32m [✔ شغال] Verdix Security Shield (سيرفر 3: درع التشفير والأدلة) \033[0m"
echo -e "\033[1;35m-----------------------------------------------------\033[0m"
echo -e "\033[1;32m [ شغال - شغال - شغال : W ] [ المنظومة كاملة نشطة ] \033[0m"
echo -e "\033[1;35m=====================================================\033[0m"

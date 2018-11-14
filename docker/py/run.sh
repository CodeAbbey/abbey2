while true; do curl http://127.0.0.1:5000/update_stats >/dev/null 2>&1; sleep 5; done &
python3 code/main.py

echo "Starting MariaDB (MySQL)..."
mysqld --user=root --datadir=/data --socket=/tmp/mysql.sock 2>/dev/null &
sleep 3
while true; do curl http://127.0.0.1:5000/update_stats >/dev/null 2>&1; sleep 10; done &
echo "Starting Python Server..."
while true; do python3 /code/main.py; read -p "Press enter to continue..."; done

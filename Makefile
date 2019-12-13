run-mitmproxy:
	mitmdump -s manage.py

up:
	docker-compose up -d

down:
	docker-compose down

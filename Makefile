up:
	docker-compose up -d

down:
	docker-compose down

mongo-cli:
	docker-compose exec mongo mongo

redis-cli:
	docker-compose exec redis redis-cli

run:
	mitmdump -s manage.py

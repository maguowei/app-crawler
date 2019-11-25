include .env

build:
	docker build -t maguowei/${APP_NAME} .

run:
	docker run -it --rm --name ${APP_NAME} -e "APP_ENV=${APP_ENV}" -p 8080:8080 \
		-v "${PWD}":/opt/app \
		maguowei/${APP_NAME}

exec:
	docker exec -it ${APP_NAME} bash

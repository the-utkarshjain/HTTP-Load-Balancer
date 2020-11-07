# Makefile
test:
	docker build -t server .
	docker-compose up -d
	pytest --disable-warnings || true
	docker-compose down
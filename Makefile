# Makefile
test:
	# docker build -t server .
	docker-compose up -d
	pytest -s --disable-warnings || true
	docker-compose down
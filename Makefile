# Makefile
test:
	rm -f logs/log.txt logs/status.txt
	# docker build -t server .
	docker-compose -f ./config/docker-compose.yaml up -d
	pytest -s --disable-warnings || true
	docker-compose -f ./config/docker-compose.yaml down

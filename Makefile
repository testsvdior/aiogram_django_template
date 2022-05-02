build:
	docker-compose -f docker-compose.prod.yaml build
prune:
	docker image prune
up:
	docker-compose -f docker-compose.prod.yaml up -d
down:
	docker-compose -f docker-compose.prod.yaml down -v
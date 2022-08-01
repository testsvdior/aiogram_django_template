build:
	docker-compose -f docker-compose.prod.yaml build
prune:
	docker image prune
up:
	docker-compose -f docker-compose.prod.yaml up -d
down:
	docker-compose -f docker-compose.prod.yaml down


redis-exec:
	docker exec -ti redis /bin/bash
redis-logs:
	docker logs redis --tail=100 -f
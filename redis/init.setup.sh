#!/bin/sh

echo "Start redis entrypoint"

sudo chmod -R a+wxr /usr/local/redis/data

##redis-server --requirepass $REDIS_PASSWORD --port $REDIS_PORT --bind $REDIS_HOST --dir /usr/local/redis/data --daemonize yes
#redis-server
redis-server /usr/local/etc/redis.conf --requirepass $REDIS_PASSWORD

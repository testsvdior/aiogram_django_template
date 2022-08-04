#!/bin/sh

echo "Start redis entrypoint"

sudo chmod -R a+wxr /usr/local/redis/data

redis-server /usr/local/etc/redis.conf

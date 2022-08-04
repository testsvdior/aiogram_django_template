FROM redis:7
COPY init.setup.sh /usr/local/redis/init.setup.sh
COPY redis.conf /usr/local/etc/redis/redis.con
#CMD [ "redis-server", "/usr/local/etc/redis.conf" ]
ENTRYPOINT ["/usr/local/redis/init.setup.sh"]

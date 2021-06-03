#!/bin/bash

docker-compose exec config-server sh -c "mongo --port 33001 < /config-server/config_server_init.js"
docker-compose exec shard1 sh -c "mongo --port 40001 < /shard1/scripts/shard1_init.js"
docker-compose exec shard2 sh -c "mongo --port 40004 < /shard2/scripts/shard2_init.js"
docker-compose exec shard2 sh -c "mongo --port 40007 < /shard3/scripts/shard3_init.js"

sleep 50
docker-compose exec mongos_router1 sh -c "mongo --port 50000 < /router/scripts/router_init.js"
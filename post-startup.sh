docker exec -it users_service alembic upgrade head
docker exec -it products_service alembic upgrade head

docker exec -i connect curl -X POST -H "Content-Type: application/json" \
  --data @/tmp/configs/elasticsearch-sink.json \
  http://localhost:8083/connectors

docker exec -i connect curl -X POST -H "Content-Type: application/json" \
  --data @/tmp/configs/postgres-source.json \
  http://localhost:8083/connectors

# docker exec minio mc alias set local https://demo13b.ddnsfree.com:9000 useradmin userpassword
# docker exec minio mc admin user add local accesskey secretkey
# docker exec minio mc admin policy attach local readwrite --user accesskey

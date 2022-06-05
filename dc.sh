if [ "`id -u`" = "0" ]
then
  /usr/bin/docker-compose "$@"
else
  docker-compose -f docker-compose-local.yaml "$@"
fi

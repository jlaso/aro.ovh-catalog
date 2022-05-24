if [ "`id -u`" = "1000" ]
then
  sudo /usr/local/bin/docker-compose "$@"
else
  docker-compose -f docker-compose-local.yaml "$@"
fi

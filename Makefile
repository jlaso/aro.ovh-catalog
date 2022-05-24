ifeq ($(server),)
    server=contabo
endif

bash:
	./dc.sh exec flask /bin/sh

rsync:
	rsync -avz --exclude-from=".rsyncignore" . $(server):/var/projects/aro.ovh

buildup:
	./dc.sh up -d --build --remove-orphans

logs:
	./dc.sh logs -f --tail=100 flask

ps:
	./dc.sh ps

down:
	./dc.sh down --remove-orphans

run-tests:
	./dc.sh exec flask /usr/local/bin/python -m unittest

up:
	sudo docker-compose up -d --build --force-recreate --remove-orphans tl_my tl_adminer

start:
	sudo docker-compose restart

stop:
	sudo docker-compose stop

run:
	sudo docker run \
		-ti --rm \
		--network tl_net \
		--name "tl_web" \
		-p 127.0.0.1:9000:9000 \
		-v $(shell pwd)/web/:/app \
		tl_scrapper_tl_web bash

up:
	sudo docker-compose up -d --build --force-recreate --remove-orphans

start:
	sudo docker-compose restart

stop:
	sudo docker-compose stop

run:
	sudo docker run \
		-ti --rm \
		--name "tl_web" \
		-p 9000:9000 \
		-v $(shell pwd)/web/:/app \
		tl_scrapper_tl_web bash

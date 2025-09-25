.PHONY: up down build backend-shell celery-shell tests

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

backend-shell:
	docker compose run --rm django /bin/bash

celery-shell:
	docker compose run --rm celery /bin/bash

tests:
	docker compose run --rm django python manage.py test

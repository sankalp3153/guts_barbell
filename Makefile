.PHONY: migrate seed test run up

migrate:
	python3 manage.py migrate

seed:
	python3 manage.py seed_sample_data

test:
	python3 manage.py test -v 2

run:
	python3 manage.py runserver 0.0.0.0:8000

up:
	docker compose up --build

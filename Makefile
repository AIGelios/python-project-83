install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: selfcheck test lint


.PHONY: install test lint selfcheck check build

dev:
	poetry run flask --app page_analyzer:app run

debug:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


db-status:
	sudo service postgresql status

db-start:
	sudo service postgresql start

db-stop:
	sudo service postgresql stop

create-tables:
	poetry run 

build:
	./build.sh
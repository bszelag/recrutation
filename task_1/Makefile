.PHONY: venv install test style all_tests run_db

venv:
	virtualenv -p python3.6 .venv
	. .venv/bin/activate
	pip install -r requirements.txt

install:
	pip install -r -q requirements.txt

test:
	pytest -v tests/

style:
	flake8 src/ tests/

all_tests: style test

run_db:
	docker pull postgres
	docker run --name ${POSTGRES_NAME} -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e POSTGRES_DB=${POSTGRES_NAME} -p 5432:5432 -v /var/run/postgresql:/var/run/postgresql -d db

run_app:
	gunicorn --reload src.app

run_all:
	. run_all.sh

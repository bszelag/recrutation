.PHONY: venv install test style all_tests

venv:
	virtualenv -p python3.6 .venv

install:
	pip install -q -r requirements.txt

test:
	pytest -v tests/

style:
	flake8 copy_titles_data.py config.py tests/

all_tests: style test

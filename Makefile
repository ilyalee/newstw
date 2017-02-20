init:
	python3 -m venv venv
	source "./venv/bin/activate"
	pip3 install -r requirements.txt

run:
	python3 crawler/crawler.py

update_deps:
	source ./venv/bin/activate
	pip3 install --upgrade -r requirements.txt

test:
	python3 -m unittest discover -s crawler/tests

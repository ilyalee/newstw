init:
	python3 -m venv venv
	source "./venv/bin/activate"
	pip3 install -r requirements.txt

run_crawler:
	python3 -O run_crawler.py

run_newsfeed:
	python3 -O run_newsfeed.py

run_fbfeed:
	python3 -O run_fbfeed.py

deps:
	pip3 freeze > ./requirements.txt

update_deps:
	source "./venv/bin/activate"
	pip3 install --upgrade -r requirements.txt

test:
	python3 -m unittest discover

init:
	python3 -m venv venv
	source "./venv/bin/activate"
	pip3 install -r requirements.txt

run_crawler:
	python3 -O run_crawler.py

run_newsfeed:
	python3 -O run_newsfeed.py

update_deps:
	source "./venv/bin/activate"
	pip3 install --upgrade -r requirements.txt

test:
	python3 -m unittest discover

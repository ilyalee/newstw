init:
	python3 -m venv venv
	source "./venv/bin/activate"
	pip3 install -r requirements.txt

pyclean:
	find . | grep -E "\(__pycache__|.pyc|.pyo$\)" | xargs rm -rf

dbclean:
	rm sqlitedb/*.db

run_crawler:
	python3 -O run_crawler.py

run_newsfeed:
	python3 -O run_newsfeed.py

run_fbfeed:
	python3 -O run_fbfeed.py

run_news_archiver:
	python3 -O run_news_archiver.py

run_scheduler:
	python3 -O scripts/scheduler.py

run_observer:
	python3 -O scripts/observer.py

run_all:
	make run_crawler >/dev/null 2>&1 &
	make run_newsfeed>/dev/null 2>&1 &
	make run_fbfeed >/dev/null 2>&1 &
	make run_news_archiver >/dev/null 2>&1 &
	make run_scheduler >/dev/null 2>&1 &

deps:
	pip3 freeze > ./requirements.txt

update_deps:
	source "./venv/bin/activate"
	pip3 install --upgrade -r requirements.txt

test:
	TESTING=1 python3 -m unittest discover

revision:
	alembic -c dev.ini revision --autogenerate

upgrade:
	alembic -c dev.ini upgrade head

downgrade:
	alembic -c dev.ini downgrade -1

reset_db:
	alembic -c dev.ini downgrade base

revision_prod:
	alembic -c prod.ini revision --autogenerate

upgrade_prod:
	alembic -c prod.ini upgrade head

downgrade_prod:
	alembic -c prod.ini downgrade head

sqlitedb:
	mkdir sqlitedb

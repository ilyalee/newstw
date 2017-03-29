init:
	python3 -m venv venv
	source "./venv/bin/activate"
	pip3 install -r requirements.txt

watch_crawler:
	watchmedo shell-command \
	  --patterns="*.html;*.css;*.js" \
	  --recursive \
	  --command='echo "${watch_src_path}" && kill -HUP `cat dev_crawler.pid`'

watch_newsfeed:
	watchmedo shell-command \
	  --patterns="*.html;*.css;*.js" \
	  --recursive \
	  --command='echo "${watch_src_path}" && kill -HUP `cat dev_newsfeed.pid`'

watch_fbfeed:
	watchmedo shell-command \
	  --patterns="*.html;*.css;*.js" \
	  --recursive \
	  --command='echo "${watch_src_path}" && kill -HUP `cat dev_fbfeed.pid`'

watch_archiver:
	watchmedo shell-command \
	  --patterns="*.html;*.css;*.js" \
	  --recursive \
	  --command='echo "${watch_src_path}" && kill -HUP `cat dev_archiver.pid`'

dev_crawler:
	gunicorn --pid=dev_crawler.pid --reload --bind localhost:9527 --worker-class sanic_gunicorn.Worker crawler.crawler:app

dev_newsfeed:
	gunicorn --pid=dev_newsfeed.pid --reload --bind localhost:9528 --worker-class sanic_gunicorn.Worker newsfeed.newsfeed:app

dev_fbfeed:
	gunicorn --pid=dev_fbfeed.pid --reload --bind localhost:9529 --worker-class sanic_gunicorn.Worker fbfeed.fbfeed:app

dev_archiver:
	gunicorn --pid=dev_archiver.pid --reload --bind localhost:9530 --worker-class sanic_gunicorn.Worker archiver.news_archive:app

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

kill_all:
	-lsof -t -i tcp:9527 | xargs kill -9
	-lsof -t -i tcp:9528 | xargs kill -9
	-lsof -t -i tcp:9529 | xargs kill -9
	-lsof -t -i tcp:9530 | xargs kill -9
	-pkill -f "make run_crawler"
	-pkill -f "make run_newsfeed"
	-pkill -f "make run_fbfeed"
	-pkill -f "make run_news_archiver"
	-pkill -f "make run_scheduler"
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

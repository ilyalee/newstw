# Python version

Use `pyenv` to install Python 3.6.1

https://github.com/pyenv/pyenv

```bash
pyenv install 3.6.1
```

### Installation

```bash
git clone https://github.com/lancetw/newstw.git
cd newstw
make install
```

### Virtual Environment

First you should activate the Python Virtual Environment:

```bash
source ./venv/bin/activate
```

### Database

Setup your database settings (Default to SQLite):

```bash
mkdir -p storage
cp alembic.ini dev.ini
cp .env.example .env
```

You should check and set `DATABASE_URL` and `FACEBOOK_ACCESS_TOKEN` in the `.env` file.

after you set up, initialize the database tables:

```bash
source .env
make revision
make upgrade
```

Congratulations, now you can run the services:

#### Web Server

```bash
make run_news_archiver
```

#### Scheduler

```bash
make run_observer
```

## Production

Follow `Installation` and `Virtual Environment` instructions.

### Database

```bash
cp alembic.ini prod.ini
cp .env.example .env
```

Modify `DATABASE_URL` and `FACEBOOK_ACCESS_TOKEN` in the `.env` file.
Modify `DELETE_KEY` if you want delete or update some articles via web APIs.

```bash
source .env
make revision
make upgrade
```

We recommend you install `circus` to run services as daemon, also see `config/circus_newstw.conf`.

https://circus.readthedocs.io
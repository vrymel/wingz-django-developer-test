## Requirements

## Setup project

### Setup environment variables
```bash
cp .env.example .env
```

Update variables in `.env` accordingly.

### Setup virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements/local.txt
```

## Run development server

```
./manage.py runserver
```

## Setup initial user

```bash
./manage.py createsuperuser
```
FROM python:3

WORKDIR /usr/src/app

COPY requirements/ requirements/
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "wingz.asgi:application"]

FROM python:3.10

WORKDIR /code
COPY . .
RUN pip install --upgrade pip && pip install -r /code/requirements.txt
CMD gunicorn friends.wsgi:application --bind 0.0.0.0:8000 --workers=6

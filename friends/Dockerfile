FROM python:3.10

WORKDIR /code
COPY . .
RUN pip3 install --upgrade pip && pip3 install -r /code/requirements.txt
CMD gunicorn friendship.wsgi:application --bind 0.0.0.0:8000 --workers=6

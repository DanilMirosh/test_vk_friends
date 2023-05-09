FROM python:3.10-slim

WORKDIR /project

EXPOSE 8000

RUN apt-get update -y  \
    && apt-get install -y --no-install-recommends curl \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt .

RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

APPLICATION_NAME = friends

run:  ##@Application Run application server
	python3 $(APPLICATION_NAME)/manage.py runserver

revision:  ##@Application Revise migrations
	python3 $(APPLICATION_NAME)/manage.py makemigrations

migrate:  ##@Application Apply migrations
	python3 $(APPLICATION_NAME)/manage.py migrate

super:  ##@Application Create superuser
	python3 $(APPLICATION_NAME)/manage.py createsuperuser

help:  ##@HELP List all possible commands
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

tests:  ##@Application Run pytest tests
	cd $(APPLICATION_NAME) && pytest -v -x

cov:  ##@Application Run pytest coverage analisys
	cd $(APPLICATION_NAME) && pytest --cov=.

lint:   ##@Application Run flake8 linter
	cd $(APPLICATION_NAME) && flake8 --max-line-len=120 --exclude migrations

build:  ##@Build Build application docker images and run
	docker compose up -d --build

up:  ##@Build Run application docker containters
	docker compose up -d

down:  ##@Build Drop application docker containters
	docker compose down

logs:  ##@Application View docker container logs
	docker compose logs

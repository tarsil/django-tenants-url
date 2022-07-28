DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean_pyc

.PHONY: clean_pyc
clean_pyc: ## Clean all *.pyc in the system
	find . -type f -name "*.pyc" -delete || true

.PHONY: migrate
migrate: # Runs the migrations
	python manage.py migrate_schemas

.PHONY: migrations
migrations: ## Generate migrations
	python manage.py makemigrations

.PHONY: requirements
requirements-deployment: ## Install the requirements
	pip install -r requirements.txt

.PHONY: test
test: ## Runs the unit tests from the scratch by recreating the testing database
	pytest $(TESTONLY) --disable-pytest-warnings -s -vv $(DB)

.PHONY: show_urls
show_urls:
	python manage.py show_urls

.PHONY: run
run:
	python manage.py runserver_plus 0.0.0.0:8000

.PHONY: shell
shell:
	python manage.py shell_plus --settings=dymmond.development.settings

.PHONY: start_docker
start_docker: ## Starts the dev environment
	docker-compose up -d

.PHONY: start_docker_logs
start_docker_logs: ## Starts the dev environment
	docker-compose up

ifndef VERBOSE
.SILENT:
endif

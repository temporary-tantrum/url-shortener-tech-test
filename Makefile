run: clean
	docker compose -f ./docker-compose-ci.yml build
	docker compose -f ./docker-compose-ci.yml up -d

clean:
	docker compose -f ./docker-compose-ci.yml down
	docker compose -f ./docker-compose-local.yml down

local: clean
	docker compose -f ./docker-compose-local up -d
	uvicorn server:app --no-use-colors

install:
	pip install -r requirements-local.txt

lint:
	pylint `git ls-files '*.py'`

test:
	pytest `git ls-files '*tests.py'`
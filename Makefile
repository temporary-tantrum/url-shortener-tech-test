build:
	docker build -t pw/url-shortener:latest .

run: build
	docker run -it --rm -p 8000:8000/tcp --name url-shortener pw/url-shortener:latest

local:
	uvicorn server:app --reload --no-use-colors

lint:
	pylint `git ls-files '*.py'`

test:
	pytest `git ls-files '*.py'`
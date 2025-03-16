format-all:
	isort .
	black . -l 120

test:
	pytest -v

run-dev:
	cd backend && uvicorn main:app --reload

run-prod:
	cd backend && uvicorn main:app
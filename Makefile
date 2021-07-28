serve:
	uvicorn app.main:app --reload

test:
	PYTHONPATH=. DATABASE_URL='postgres://postgres:postgres@localhost:5432/tdeexchange_test' pytest

test_loud:
	PYTHONPATH=. DATABASE_URL='postgres://postgres:postgres@localhost:5432/tdeexchange_test' pytest -s

shell:
	python manage.py

pulldb:
	-docker start tde-postgres
	-docker exec -e PGPASSWORD='postgres' -it tde-postgres dropdb tdeexchange -Upostgres
	PGPASSWORD='postgres' heroku pg:pull DATABASE_URL "postgresql://postgres@localhost:5432/tdeexchange?sslmode=disable"

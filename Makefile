serve:
	uvicorn app.main:app --reload

test:
	PYTHONPATH=. DATABASE_URL='postgres://postgres:postgres@localhost:5432/tdeexchange_test' pytest

test_loud:
	PYTHONPATH=. DATABASE_URL='postgres://postgres:postgres@localhost:5432/tdeexchange_test' pytest -s

shell:
	piccolo shell run

serve:
	uvicorn app.main:app --reload

test:
	PYTHONPATH=. pytest

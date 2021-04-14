release: PICCOLO_CONF="app.piccolo_conf" piccolo migrations forwards all
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}

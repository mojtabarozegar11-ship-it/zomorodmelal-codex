install:
	python -m pip install -r requirements-host.txt

check:
	python manage.py check

deploy-check:
	python manage.py check --deploy

migrate:
	python manage.py migrate

static:
	python manage.py collectstatic --noinput

test:
	python manage.py test

health:
	python manage.py check

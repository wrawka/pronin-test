django-migrate:
	uv run python proninteam_backend/manage.py makemigrations
	uv run python proninteam_backend/manage.py migrate

django-test-data:
	uv run python proninteam_backend/manage.py populate_mock_data

django-dev-server:
	uv run python proninteam_backend/manage.py runserver 0.0.0.0:8000

django-static-collect:
	uv run python proninteam_backend/manage.py collectstatic --noinput

django-prod-server:
	cd proninteam_backend && \
	uv run gunicorn --bind 0.0.0.0:8000 config.wsgi:application

django-start: django-migrate django-test-data django-static-collect django-prod-server

celery-start:
	cd proninteam_backend && \
	uv run celery -A config worker --loglevel=info

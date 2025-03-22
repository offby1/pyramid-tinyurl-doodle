FROM python:3.12-slim-bullseye
RUN pip install --upgrade pip
RUN pip install poetry
COPY . /django-project
WORKDIR /django-project
ENV DJANGO_SETTINGS_MODULE=project.prod_settings
RUN poetry install
RUN poetry run python3 manage.py makemigrations
RUN poetry run python3 manage.py migrate
RUN poetry run python3 manage.py collectstatic --no-input

# https://github.com/django/daphne/pull/520
env PYTHONUNBUFFERED=t

CMD poetry run  daphne --verbosity  3 --bind 0.0.0.0 --port 8000  --log-fmt="%(asctime)sZ %(levelname)s %(name)s %(filename)s %(funcName)s %(message)s" project.asgi:application

FROM python:3.12-slim-bullseye
RUN pip install --upgrade pip
RUN pip install poetry
COPY . /django-project
WORKDIR /django-project
ENV DJANGO_SETTINGS_MODULE=project.prod_settings
RUN poetry install
RUN poetry run python3 manage.py makemigrations
RUN poetry run python3 manage.py migrate
RUN DJANGO_SUPERUSER_PASSWORD=admin poetry run python3 manage.py createsuperuser --no-input --username=admin --email=admin@admin.com
RUN poetry run python3 manage.py collectstatic --no-input
CMD poetry run gunicorn --bind 0.0.0.0:8000  --log-level=DEBUG project.wsgi
# run with docker run  --publish 8000:8000  -it deadbeef

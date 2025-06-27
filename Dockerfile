FROM python:3.12-slim-bullseye AS build

# https://github.com/django/daphne/pull/520
ENV PYTHONUNBUFFERED=t \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1

RUN pip install --upgrade pip
RUN pip install poetry

COPY /.git-post-checkout-info /django-project/
COPY /app/                    /django-project/app/
COPY /manage.py               /django-project/
COPY /poetry.lock             /django-project/
COPY /project/                /django-project/project/
COPY /pyproject.toml          /django-project/
COPY /start-daphne.sh         /django-project/

WORKDIR /django-project
RUN poetry install

FROM python:3.12-slim-bullseye AS app
COPY --from=build /django-project/ /django-project/
WORKDIR /django-project

ENV DJANGO_SETTINGS_MODULE=project.prod_settings

CMD ["/bin/bash", "-c", "./start-daphne.sh"]

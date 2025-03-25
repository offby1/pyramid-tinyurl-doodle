FROM python:3.12-slim-bullseye AS build

# https://github.com/django/daphne/pull/520
ENV PYTHONUNBUFFERED=t \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1

RUN pip install --upgrade pip
RUN pip install poetry
COPY . /django-project
WORKDIR /django-project
RUN poetry install

FROM python:3.12-slim-bullseye AS app
COPY --from=build /django-project/.venv/ /django-project/.venv/
COPY --from=build /django-project/manage.py /django-project/
COPY --from=build /django-project/app/ /django-project/app/
COPY --from=build /django-project/project/ /django-project/project/
WORKDIR /django-project

ENV DJANGO_SETTINGS_MODULE=project.prod_settings

RUN /django-project/.venv/bin/python3 manage.py makemigrations
RUN /django-project/.venv/bin/python3 manage.py migrate
RUN /django-project/.venv/bin/python3 manage.py collectstatic --no-input

CMD ["/django-project/.venv/bin/daphne", \
    "--verbosity", \
    "3", \
    "--bind", \
    "0.0.0.0", \
    "--port", \
    "8000", \
    "--log-fmt=\"%(asctime)sZ %(levelname)s %(name)s %(filename)s %(funcName)s %(message)s\"", "project.asgi:application" \
    ]

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
COPY --from=build /django-project/app/ /django-project/app/
COPY --from=build /django-project/manage.py /django-project/
COPY --from=build /django-project/project/ /django-project/project/
COPY --from=build /django-project/start-daphne.sh /django-project/
WORKDIR /django-project

ENV DJANGO_SETTINGS_MODULE=project.prod_settings

CMD ["/bin/bash", "-c", "./start-daphne.sh"]

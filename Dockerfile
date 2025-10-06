FROM python:3.12-slim-bullseye AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# https://github.com/django/daphne/pull/520
ENV PYTHONUNBUFFERED=t

COPY /.git-post-checkout-info /django-project/
COPY /app/                    /django-project/app/
COPY /manage.py               /django-project/
COPY /uv.lock                 /django-project/
COPY /project/                /django-project/project/
COPY /pyproject.toml          /django-project/
COPY /start-daphne.sh         /django-project/

WORKDIR /django-project
RUN uv sync

FROM python:3.12-slim-bullseye AS app
COPY --from=build /django-project/ /django-project/
WORKDIR /django-project

ENV DJANGO_SETTINGS_MODULE=project.prod_settings

CMD ["/bin/bash", "-c", "./start-daphne.sh"]

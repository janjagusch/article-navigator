FROM python:3.8.6-slim-buster AS build-env

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION="1.0.10"
ENV POETRY_VIRTUALENVS_CREATE="false"

RUN set -ex \
    && apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y libev-dev g++ curl git make \
    && curl -sSL \
    https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && pip install --upgrade pip gunicorn \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

WORKDIR /usr/src/app

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN . $HOME/.poetry/env \
    && poetry install --no-dev

COPY . .

EXPOSE 8080

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

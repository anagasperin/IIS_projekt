FROM python:3.10.

WORKDIR /src

COPY pyproject.toml poetry.lock /tmp/poetry/

ENV POETRY_VERSION=1.0

RUN pip install "poetry==$POETRY_VERSION"

CMD python server/server.py

EXPOSE 5000
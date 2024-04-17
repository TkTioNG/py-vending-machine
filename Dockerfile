
FROM python:3.11-slim

RUN pip3 install --upgrade pip
RUN pip3 install poetry

WORKDIR /app/

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-directory --no-interaction

COPY . /app/

FROM python:3.13-slim

ENV PATH="/scripts:${PATH}"
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1

RUN pip install poetry

RUN mkdir -p /app/mock_service
COPY ./mock_service /app/mock_service

WORKDIR /app
COPY __init__.py .
COPY manage.py .
COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN mkdir scripts
COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN adduser appuser
RUN chown -R appuser:appuser /app

USER appuser
RUN poetry install --without dev
CMD ["start.sh"]

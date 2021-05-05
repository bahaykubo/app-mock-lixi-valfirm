FROM python:3.7-slim

ENV PATH="/scripts:${PATH}"
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_VERBOSITY=-1

RUN pip install pipenv

RUN mkdir -p /app/mock_service
COPY ./mock_service /app/mock_service

WORKDIR /app
COPY __init__.py .
COPY manage.py .
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN mkdir scripts
COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN adduser appuser
RUN chown -R appuser:appuser /app

USER appuser
RUN pipenv install
CMD ["start.sh"]

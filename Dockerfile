FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install asyncpg

COPY ./app /app
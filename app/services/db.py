import asyncpg
import logging as log
from fastapi import HTTPException
from os import getenv

async def connect() -> asyncpg.Connection:
    database = getenv("POSTGRES_DB")
    host = getenv("POSTGRES_HOST")
    password = getenv("POSTGRES_PASSWORD")
    user = getenv("POSTGRES_USER")

    log.info("connecting to database %s on host %s", database, host)
    conn = await asyncpg.connect(host=host, port=5432, user=user, password=password, database=database)
    try:
        types = await conn.fetch("select * from pg_type")
        if not types:
            raise HTTPException(status_code=500, detail="could not connect to postgres")
        yield conn
    finally:
        log.info("closing database connection...")
        await conn.close()
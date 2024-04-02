from fastapi import FastAPI
from sqlalchemy_utils import create_database, database_exists

from app.api.router import router
from app.db.db import Engine

if not database_exists(Engine.url):
    create_database(Engine.url)

app = FastAPI(
    title='splitfood',
    version='1.0',
    description='python api for splitfood app'
)

app.include_router(router)

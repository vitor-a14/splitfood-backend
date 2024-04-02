import uvicorn
from app.app import app
from app.db.db import Engine, Base
from sqlalchemy_utils import create_database, database_exists


def initiate_database():
    if not database_exists(Engine.url):
        create_database(Engine.url)
    Base.metadata.create_all(bind=Engine)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
    initiate_database()

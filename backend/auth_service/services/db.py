from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config.settings import settings


client = MongoClient(settings.mongo_url)
db = client[settings.database_name]


def ensure_indexes() -> None:
    try:
        db.users.create_index("email", unique=True)
    except PyMongoError:
        # Service should still boot even if DB isn't up yet.
        pass

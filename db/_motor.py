import motor.motor_asyncio
import os
import logger

col = {}


def connect():
    logger.log("Motor is initialized")
    client = motor.motor_asyncio.AsyncIOMotorClient(
        os.environ['MONGO_URL']
    )
    db = client["Bot"]
    global collections
    col["yam"] = db["Yam"]
    return col["yam"]


def get_col():
    return col.get("yam") or connect()


async def insert(data):
    return await get_col().insert_one(data)


async def find(data):
    return await get_col().find_one(data)

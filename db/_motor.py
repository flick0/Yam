import motor.motor_asyncio
import os
import logger


class mongo:
    def __init__(self):
        logger.log("Motor is initialized")
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            os.environ['MONGO_URL']
        )
        self.db = self.client["Bot"]
        self.col = self.db["Yam"]

    async def insert(self, data):
        await self.col.insert_one(data)

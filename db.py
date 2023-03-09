import motor.motor_asyncio
from settings import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
db = client[settings.database_name]

from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from beanie import init_beanie 
from app.config import settings
import certifi 

async def init_db():
    # Pass certifi's CA bundle to ensure SSL certificates are verified correctly
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tls=True,
        tlsCAFile=certifi.where()  # <-- fixes SSL certificate verify failed error
    )
    db = client["Placement-buddy"]

    # import document models here so they register
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.analysis import Analysis

    await init_beanie(database=db, document_models=[User, Resume, Analysis])

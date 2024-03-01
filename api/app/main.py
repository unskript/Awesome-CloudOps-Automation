from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

from db.database import Base, engine
from api.endpoints.item import items_router
from api.endpoints.user import users_router


app = FastAPI()



DB_URL = os.getenv("DB_URL")
print("DB_URL = os.getenv: ", DB_URL)

Base.metadata.create_all(bind=engine)


# Include API routers
app.include_router(items_router)
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI
from dotenv import load_dotenv
# Load .env file
load_dotenv()

from api.endpoints.suite import suite_router

app = FastAPI()

# Include API routers
app.include_router(suite_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

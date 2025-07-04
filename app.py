import os
import uvicorn
from src.local_log.log import logger
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.token_validator import get_token_header
from src.routers import api
from dotenv import load_dotenv

# from decouple import config


load_dotenv()  # Load environment variables from .env file
# os.environ["OPENAI_API_KEY"] = str(config("OPENAI_API_KEY"))

AppURL = os.getenv("APP_URL")

app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Application"),
    description=os.getenv("APP_DESCRIPTION", "A FastAPI application with CORS and token validation"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    dependencies=[Depends(get_token_header)],
    # servers=[
    #         {"url": "http://"+AppURL+":8000", "description": "Staging environment"},
    #         # {"url": "https://prod.example.com", "description": "Production environment"},
    #     ],
)


origins = [
    # "http://10.255.254.26:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router)


def run():
    """Launched with `poetry run start` at root level"""
    app_url = os.getenv("APP_URL")

    if not app_url:
        logger.log("error", "APP_URL environment variable is not set.")
        return
    # Expecting format like "127.0.0.1:8000"
    if ":" in app_url:
        host, port = app_url.split(":")
    else:
        host, port = app_url, 8000

    try:
        uvicorn.run("app:app", host=host, port=int(port), reload=True)
    except Exception as e:
        logger.log("error", f"Failed to start server: {e}")


if __name__ == "__main__":
    run()

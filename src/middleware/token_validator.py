import os
from typing import Annotated

from fastapi import Header, HTTPException
from dotenv import load_dotenv

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != os.getenv("APP_KEY"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")

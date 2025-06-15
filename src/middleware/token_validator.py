from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "ED2M4WSXGKiS3dXPqztNbi3M5YmaRbu7X":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

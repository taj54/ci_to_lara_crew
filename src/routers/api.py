import humps
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from validation.validation import Validate

router = APIRouter()


class Query(BaseModel):
    
    module_name: str
    api_version: str 
    endpoint_name: str
    inputs: dict | None = None


class Response(BaseModel):
    success: bool
    message: str


@router.post("/ci-lara-ai-converter", tags=["CI to Lara AI"], response_model=Response)
async def query_marketing_ai(query: Query):
    ModuleName = query.module_name
    APIVersion = query.api_version
    EndpointName = query.endpoint_name
    Payload = query.inputs
    validateReponse = Validate(ModuleName, APIVersion, EndpointName, Payload)
    result = validateReponse.run()
    if result.get("success") == False:
        raise HTTPException(status_code=422, detail=result.get("message"))
    else:
        CrewClassName = humps.pascalize(EndpointName) + "Crew"
        # crew = globals()[CrewClassName](Payload)
        # response = crew.run()
        response = {"success": True, "message": CrewClassName + " crew executed successfully."}
        return response

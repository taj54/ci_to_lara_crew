import humps
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from validation.migration_validator import MigrationValidator

router = APIRouter()


class Query(BaseModel):
    
    migration_direction: str
    source_version: str
    target_version: str
    inputs: dict | None = None


class Response(BaseModel):
    success: bool
    message: str

@router.post("/ci-lara-ai-converter", tags=["CI to Lara AI"], response_model=Response)
async def query_marketing_ai(query: Query):
    MigrationDirection = query.migration_direction
    SourceVersion = query.source_version
    TargetVersion = query.target_version
    payload = query.inputs
    validateReponse = MigrationValidator(MigrationDirection, SourceVersion, TargetVersion, payload)
    result = validateReponse.run()
    if result.get("success") == False:
        raise HTTPException(status_code=422, detail=result.get("message"))
    else:
        CrewClassName = humps.pascalize(TargetVersion) + "Crew"
        # crew = globals()[CrewClassName](Payload)
        # response = crew.run()
        response = {"success": True, "message": CrewClassName + " crew executed successfully."}
        return response

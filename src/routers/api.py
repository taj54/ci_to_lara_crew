import humps
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from factories.centralized_crew_factory import CrewFactory
from local_log.log import logger  

from validation.migration_validator import MigrationValidator

router = APIRouter(
    prefix="/ci-lara-ai-converter",
    tags=["CI to Lara AI"]
)
CrewFactory.initialize()

class Query(BaseModel):
    migration_direction: str
    source_version: str
    target_version: str
    inputs: dict | None = None

class Response(BaseModel):
    success: bool
    message: str

def handle_action(query: Query, action: str, success_msg: str):
    MigrationDirection = query.migration_direction
    SourceVersion = query.source_version
    TargetVersion = query.target_version
    Payload = query.inputs
    validate_response = MigrationValidator(MigrationDirection, SourceVersion, TargetVersion, Payload)
    result = validate_response.run()
    if not result.get("success"):
        raise HTTPException(status_code=422, detail=result.get("message"))
    CrewClassName = humps.pascalize(SourceVersion.replace(".", "_")+"To"+TargetVersion.replace(".", "_"))
    CrewClassName = CrewClassName.lower()
    crew = CrewFactory.get_crew(CrewClassName, Payload)
    if not crew:
        raise HTTPException(
            status_code=422, detail="Crew not found or failed to instantiate."
        )
    getattr(crew, action)()
    return {"success": True, "message": f"{CrewClassName} crew {success_msg} successfully."}

@router.post("/run", response_model=Response)
async def query_ci_lara_ai(query: Query):
    return handle_action(query, "run", "executed")

@router.post("/train", response_model=Response)
async def train_ci_lara_ai(query: Query):
    return handle_action(query, "train", "trained")

@router.post("/replay", response_model=Response)
async def replay_ci_lara_ai(query: Query):
    return handle_action(query, "replay", "replayed")

@router.post("/test", response_model=Response)
async def test_ci_lara_ai(query: Query):
    return handle_action(query, "test", "tested")

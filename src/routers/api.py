import humps
from fastapi import APIRouter, HTTPException,Form
from pydantic import BaseModel
from src.factories.centralized_crew_factory import CrewFactory
from src.local_log.log import logger

from src.validation.migration_validator import MigrationValidator
from fastapi import File, UploadFile
import json

router = APIRouter(prefix="/ci-lara-ai-converter", tags=["CI to Lara AI"])
CrewFactory.initialize()


class Query(BaseModel):
    migration_direction: str
    source_version: str
    target_version: str

class RunQuery(Query):
    inputs: dict | None = None

class TrainQuery(Query):
    train_data: dict | None = None

class Response(BaseModel):
    success: bool
    message: str


def handle_action(query, action: str, success_msg: str):
    MigrationDirection = query.migration_direction
    SourceVersion = query.source_version
    TargetVersion = query.target_version
    Payload = query.inputs
    validate_response = MigrationValidator(
        MigrationDirection, SourceVersion, TargetVersion, Payload
    )

    result = validate_response.run()
    if not result.get("success"):
        raise HTTPException(status_code=422, detail=result.get("message"))

    CrewClassName = humps.pascalize(
        SourceVersion.replace(".", "_") + "To" + TargetVersion.replace(".", "_")
    )
    CrewClassName = CrewClassName.lower()
    newPayload = {
        **(Payload or {}),
        "source_version": SourceVersion,
        "target_version": TargetVersion,
    }
    crew = CrewFactory.get_crew(CrewClassName, newPayload)
    if not crew:
        raise HTTPException(
            status_code=422, detail="Crew not found or failed to instantiate."
        )
    getattr(crew, action)()
    return {
        "success": True,
        "message": f"{CrewClassName} crew {success_msg} successfully.",
    }


@router.post("/run", response_model=Response)
async def query_ci_lara_ai(query: RunQuery):
    return handle_action(query, "run", "executed")


@router.post("/train", response_model=Response)
async def train_ci_lara_ai(
    query: str = Form(...), 
    file: UploadFile = File(...)
):
    try:
        # Parse the query JSON string to a dict
        query_dict = json.loads(query)
        file_content = await file.read()
        train_data = json.loads(file_content)
        query_dict["train_data"] = train_data
        query_obj = TrainQuery(**query_dict)
        logger.log("info", f"Parsed query object: {query_obj}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    return handle_action(query_obj, "train", "trained")


@router.post("/replay", response_model=Response)
async def replay_ci_lara_ai(query: Query):
    return handle_action(query, "replay", "replayed")


@router.post("/test", response_model=Response)
async def test_ci_lara_ai(query: Query):
    return handle_action(query, "test", "tested")

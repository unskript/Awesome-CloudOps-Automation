from fastapi import APIRouter
from api.schemas.suite import CreateSuiteResponse, CreateSuiteRequest
from api.service import suite_service

suite_router = APIRouter()

@suite_router.post("/suites", response_model=CreateSuiteResponse)
def create_suite(request: CreateSuiteRequest):
    return suite_service.create_suite(suite=request)

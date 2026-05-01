from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.statistics_service import StatisticsService
from app.presentation.dependencies import get_statistics_service, get_current_user_id
from app.presentation.mappers.statistics_mapper import _to_detection_log_response, _to_statistics_response

router = APIRouter(prefix="/statistics", tags=["statistics"],
    dependencies=[Depends(get_current_user_id)])

@router.get("")
def get_detection_logs(
    search: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    limit: int = 10,
    skip: int = 0,
    order: str = "desc",
    status: str | None = None,
    service: StatisticsService = Depends(get_statistics_service),
):
    try:
        detection_log = service.get_detection_logs(search, start_time, end_time, limit, skip, order, status)
        return _to_detection_log_response(detection_log)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard")
def get_statistics(
    start_time: str | None = None,
    end_time: str | None = None,
    service: StatisticsService = Depends(get_statistics_service)
):
    try:
        statistics = service.get_statistics(start_time, end_time)
        return _to_statistics_response(statistics)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
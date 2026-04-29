from app.domain.repositories.statistics import StatisticsRepository
from app.application.dto.statistics_dto import DetectionLogDTO
from app.application.mappers.statistics_mapper import _to_detection_log_dto
from app.application.mappers.detection_mapper import _status_text_to_id

class StatisticsService:
    def __init__(self, statistic_repository: StatisticsRepository):
        self.repo = statistic_repository

    def get_detection_logs(
        self, 
        search: str,
        start_time: str, 
        end_time: str,
        limit: str,
        skip: str,
        order: str,
        status: str
    ) -> DetectionLogDTO:
        detection_log = self.repo.get_detection_logs(search, start_time, end_time, limit, skip, order, _status_text_to_id(status))

        if detection_log is None:
            raise ValueError("Prescriptions not found")
        
        return _to_detection_log_dto(detection_log)
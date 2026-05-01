from app.domain.repositories.statistics import StatisticsRepository
from app.domain.constants.order_status import STATUS_GROUP
from app.application.dto.statistics_dto import DetectionLogDTO, StatisticsDTO
from app.application.mappers.statistics_mapper import _to_detection_log_dto, _to_statistics_dto
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
        status: str,
        error_type: str,
        month_key: str
    ) -> DetectionLogDTO:
        statuses = STATUS_GROUP.get(status, [])
        detection_log = self.repo.get_detection_logs(search, start_time, end_time, limit, skip, order, statuses, error_type, month_key)

        if detection_log is None:
            raise ValueError("Prescriptions not found")
        
        return _to_detection_log_dto(detection_log)
    
    def get_statistics(
            self,
            start_time: str,
            end_time: str
    ) -> StatisticsDTO:
        status_summary = self.repo.get_order_status_statistics(start_time, end_time)
        error_summary = self.repo.get_error_statistics(start_time, end_time)
        annual_summary = self.repo.get_annual_error_statistics()

        return _to_statistics_dto(status_summary, error_summary, annual_summary)
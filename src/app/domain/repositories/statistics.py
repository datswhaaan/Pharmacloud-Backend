from abc import abstractmethod
from app.domain.entities.statistics import DetectionLog

class StatisticsRepository:
    @abstractmethod
    def get_detection_logs(
        self,
        search: str,
        start_time: str,
        end_time: str,
        limit: str,
        skip: str,
        order: str,
        status: str
    ) -> DetectionLog:
        '''Retrieve paginated detection logs with optional filtering by search, time range, status, and sorting order.'''
        raise
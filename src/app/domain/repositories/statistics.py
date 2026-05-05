from abc import abstractmethod
from app.domain.entities.statistics import DetectionLog, Summary

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
        statuses: list[str],
        error_type: str,
        month_key: str
    ) -> DetectionLog:
        '''Retrieve paginated detection logs with optional filtering by search, time range, status, and sorting order.'''
        raise NotImplementedError

    @abstractmethod
    def get_order_status_statistics(
        self,
        start_time: str,
        end_time: str,
    ) -> Summary:
        """Return aggregated order status counts within the specified time range."""
        raise NotImplementedError

    @abstractmethod
    def get_error_statistics(
        self,
        start_time: str,
        end_time: str,
    ) -> Summary:
        """Return summary of error types (e.g., wrong name, quantity) within the specified time range."""
        raise NotImplementedError

    @abstractmethod
    def get_annual_error_statistics(self) -> Summary:
        """Return monthly error trends for the past 12 months."""
        raise NotImplementedError
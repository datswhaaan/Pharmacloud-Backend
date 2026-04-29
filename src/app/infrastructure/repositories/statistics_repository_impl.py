from sqlalchemy import case
from sqlalchemy.orm import Session, selectinload
from app.domain.repositories.statistics import StatisticsRepository
from app.domain.entities.statistics import DetectionLog
from app.infrastructure.models.detection import DetectionORM, OrderORM, OrderStatusORM, VisitORM, PatientORM, PatientPrefixORM, EmployeeORM
from app.infrastructure.mappers.statistics_mapper import _to_detection_log

class StatisticsRepositoryImpl(StatisticsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_detection_logs(
        self,
        search: str,
        start_time: str,
        end_time: str,
        limit: int,
        skip: int,
        order: str,
        status: str
    ) -> DetectionLog :
        query = (
            self.session
            .query(DetectionORM)
            .join(DetectionORM.orders)
            .join(OrderORM.visit)
            .join(OrderORM.status)
            .options(
                selectinload(DetectionORM.orders)
                    .selectinload(OrderORM.visit)
                    .selectinload(VisitORM.patient)
            )
        )
        
        if search:
            query = query.filter(
                VisitORM.visit_hn.ilike(f"%{search}%") |
                VisitORM.visit_vn.ilike(f"%{search}%") |
                PatientORM.patient_firstname.ilike(f"%{search}%") |
                PatientORM.patient_lastname.ilike(f"%{search}%") |
                EmployeeORM.employee_firstname.ilike(f"%{search}%") |
                EmployeeORM.employee_lastname.ilike(f"%{search}%")
            )

        if status:
            query = query.filter(DetectionORM.status_id == status)

        if start_time:
            query = query.filter(VisitORM.visit_begin_visit_time >= start_time)

        if end_time:
            query = query.filter(VisitORM.visit_begin_visit_time <= end_time)
        
        total = query.distinct().count()

        rows = (
            query
            .order_by(
                VisitORM.visit_begin_visit_time.asc()
                if order == "asc"
                else VisitORM.visit_begin_visit_time.desc()
            )
            .limit(limit)
            .offset(skip)
            .all()
        )

        page = (skip // limit) + 1 if limit else 1

        return _to_detection_log(rows, total, page, min(limit, total - skip))
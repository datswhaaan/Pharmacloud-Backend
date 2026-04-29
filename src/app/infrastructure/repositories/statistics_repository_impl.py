from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session, selectinload
from app.domain.repositories.statistics import StatisticsRepository
from app.domain.entities.statistics import DetectionLog, Summary
from app.infrastructure.models.detection import DetectionORM, DetectionItemORM, OrderORM, OrderStatusORM, VisitORM, PatientORM, EmployeeORM
from app.infrastructure.mappers.statistics_mapper import _to_detection_log, _to_error_summary, _to_status_summary, _to_annual_error_summary

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

    def get_order_status_statistics(
        self,
        start_time: str,
        end_time: str,
    ) -> Summary:
        query = (
            self.session.query(
                OrderStatusORM.order_status_description.label("label"),
                func.count().label("count")
            )
            .join(OrderORM, OrderStatusORM.f_order_status_id == OrderORM.f_order_status_id)
            .group_by(OrderStatusORM.f_order_status_id)
        )

        if start_time:
            query = query.filter(VisitORM.visit_begin_visit_time >= start_time)

        if end_time:
            query = query.filter(VisitORM.visit_begin_visit_time <= end_time)

        rows = query.all()

        return _to_status_summary(rows)

    def get_error_statistics(
        self,
        start_time: str,
        end_time: str,
    ) -> Summary:
        query = (
            self.session.query(
                DetectionItemORM.error_type.label("label"),
                func.count().label("count")
            )
            .group_by(DetectionItemORM.error_type)
        )

        if start_time:
            query = query.filter(VisitORM.visit_begin_visit_time >= start_time)

        if end_time:
            query = query.filter(VisitORM.visit_begin_visit_time <= end_time)

        rows = query.all()

        return _to_error_summary(rows)

    def get_annual_error_statistics(self) -> Summary:
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=11)

        query = (
            self.session.query(
                func.date_trunc("month", DetectionORM.created_at).label("month"),
                func.count().label("count")
            )
            .join(DetectionORM.detection_item)
            .filter(
                DetectionORM.created_at >= start_date,
                DetectionORM.created_at <= end_date
            )
            .group_by("month")
            .order_by("month")
        )

        query = query.filter(
            or_(
                and_(
                    DetectionItemORM.match_type == "MATCHED",
                    DetectionItemORM.is_manually_edited == True
                ),
                and_(
                    DetectionItemORM.match_type == "EXTRA",
                    DetectionItemORM.is_manually_edited == False
                )
            )
        )

        rows = query.all()

        return _to_annual_error_summary(rows)
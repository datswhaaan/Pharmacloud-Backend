from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, func, cast, DateTime
from sqlalchemy.orm import Session
from app.domain.repositories.statistics import StatisticsRepository
from app.domain.entities.statistics import DetectionLog, Summary
from app.infrastructure.models.detection import DetectionORM, DetectionItemORM, OrderORM, OrderStatusORM, VisitORM, PatientORM, EmployeeORM, PatientPrefixORM
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
        status: list[str],
        error_type: str,
        month_key: str | None = None
    ) -> DetectionLog :
        query = (
            self.session
            .query(DetectionORM)
            .join(DetectionORM.orders)
            .join(OrderORM.visit)
            .join(VisitORM.patient)
            .outerjoin(PatientORM.prefix) 
            .outerjoin(EmployeeORM, DetectionORM.verified_by == EmployeeORM.b_employee_id)
            .filter(DetectionORM.status != "UNVERIFIED")
        )
        
        if search:
            query = query.filter(
                VisitORM.visit_hn.ilike(f"%{search}%") |
                VisitORM.visit_vn.ilike(f"%{search}%") |
                PatientPrefixORM.patient_prefix_description.ilike(f"%{search}%") |
                PatientORM.patient_firstname.ilike(f"%{search}%") |
                PatientORM.patient_lastname.ilike(f"%{search}%") |
                EmployeeORM.employee_firstname.ilike(f"%{search}%") |
                EmployeeORM.employee_lastname.ilike(f"%{search}%")
            )

        if len(status) > 0:
            query = query.filter(
                OrderORM.f_order_status_id.in_(status)
            )
        if error_type :
            query = query.filter(
                DetectionORM.detection_item.any(
                    DetectionItemORM.error_type == error_type
                )
            )

        if month_key:
            year, month = month_key.split("-")

            query = query.filter(
                extract('year', DetectionORM.created_at) == int(year),
                extract('month', DetectionORM.created_at) == int(month)
            )

        else:
            if start_time:
                start_dt = datetime.fromisoformat(start_time)
                query = query.filter(DetectionORM.detected_at >= start_dt)

            if end_time:
                end_dt = datetime.fromisoformat(end_time) + timedelta(days=1)
                query = query.filter(DetectionORM.detected_at < end_dt)

        
        total = query.distinct().count()

        rows = (
            query
            .order_by(
                DetectionORM.detected_at.asc()
                if order == "asc"
                else DetectionORM.detected_at.desc()
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
                func.date_trunc("month", DetectionORM.verified_at).label("month"),
                func.count().label("count")
            )
            .join(DetectionORM.detection_item)
            .filter(
                DetectionORM.verified_at >= start_date,
                DetectionORM.verified_at <= end_date
            )
            .group_by("month")
            .order_by("month")
        )

        query = query.filter(DetectionItemORM.match_type == "EXTRA")

        rows = query.all()

        return _to_annual_error_summary(rows)
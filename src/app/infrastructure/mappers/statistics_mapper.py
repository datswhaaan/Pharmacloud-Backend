from app.infrastructure.models.detection import DetectionORM
from app.domain.entities.statistics import DetectionLog, DetectionLogItem

def _to_detection_log_item(log: DetectionORM) -> DetectionLogItem:
    return DetectionLogItem(
        detection_id=log.detection_id,
        visit_hn=log.orders.visit.visit_hn,
        visit_vn=log.orders.visit.visit_vn,
        patient_prefix=log.orders.visit.patient.prefix.patient_prefix_description,
        patient_firstname=log.orders.visit.patient.patient_firstname,
        patient_lastname=log.orders.visit.patient.patient_lastname,
        employee_firstname=log.employee.employee_firstname if log.employee else "",
        employee_lastname=log.employee.employee_lastname if log.employee else "",
        verified_at=log.verified_at if log.verified_at else ""
    )

def _to_detection_log(detections: list[DetectionORM], total: int, page: int, size: int) -> DetectionLog:
    return DetectionLog(
        detections=[_to_detection_log_item(log) for log in detections],
        total=total,
        page=page,
        size=size
    )
from app.infrastructure.models.detection import DetectionORM
from app.domain.entities.statistics import DetectionLog, DetectionLogItem, Summary

def _to_detection_log_item(log: DetectionORM) -> DetectionLogItem:
    return DetectionLogItem(
        detection_id=log.detection_id,
        order_id=log.t_order_id,
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

def _to_status_summary(orms) -> Summary:
    completed = 0
    waited = 0
    cancel = 0

    for orm in orms:
        if orm.label in ["ยืนยัน", "รายงานผล", "จ่าย"]:
            completed += orm.count
        elif orm.label in ["ดำเนินการ", "ค้างรายงานผล"]:
            waited += orm.count
        elif orm.label == "ยกเลิก":
            cancel += orm.count

    return Summary(
        label=["ตรวจสอบสำเร็จ", "รอตรวจสอบ", "ยกเลิก"],
        value=[completed, waited, cancel]
    )

def _to_error_summary(orms) -> Summary:
    wrong_name = 0
    wrong_strength = 0
    wrong_quantity = 0
    wrong_form = 0

    for orm in orms:
        if orm.label == "WRONG_DRUG_NAME":
            wrong_name = orm.count
        elif orm.label == "WRONG_STRENGTH":
            wrong_strength = orm.count
        elif orm.label == "WRONG_QUANTITY":
            wrong_quantity = orm.count
        elif orm.label == "WRONG_FORM":
            wrong_form = orm.count

    return Summary(
        label=["ผิดชื่อยา", "ผิดความแรง", "ผิดจำนวน", "ผิดรูปแบบ"],
        value=[wrong_name, wrong_strength, wrong_quantity, wrong_form]
    )

def _to_annual_error_summary(rows) -> Summary:
    return Summary(
        label=[row.month.strftime("%b") for row in rows],
        value=[row.count for row in rows]
    )
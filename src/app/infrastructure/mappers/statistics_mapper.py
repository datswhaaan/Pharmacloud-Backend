from calendar import month_abbr
from datetime import datetime
from app.infrastructure.models.detection import DetectionORM
from app.domain.entities.statistics import DetectionLog, DetectionLogItem, Summary, SummaryItem

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
        verified_at=log.verified_at.strftime("%Y-%m-%d %H:%M:%S") if log.verified_at else ""
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
    waiting = 0
    cancel = 0

    for orm in orms:
        if orm.label in ["ยืนยัน", "รายงานผล", "จ่าย"]:
            completed += orm.count
        elif orm.label in ["ดำเนินการ", "ค้างรายงานผล"]:
            waiting += orm.count
        elif orm.label == "ยกเลิก":
            cancel += orm.count

    return Summary(
        data=[
            SummaryItem(key="COMPLETED", label="ตรวจสอบสำเร็จ", value=completed),
            SummaryItem(key="WAITING", label="รอตรวจสอบ", value=waiting),
            SummaryItem(key="CANCELLED", label="ยกเลิก", value=cancel),
        ]
    )

def _to_error_summary(orms) -> Summary:
    wrong_drug_name = 0
    wrong_strength = 0
    wrong_quantity = 0
    wrong_form = 0

    for orm in orms:
        if orm.label == "WRONG_DRUG_NAME":
            wrong_drug_name = orm.count
        elif orm.label == "WRONG_STRENGTH":
            wrong_strength = orm.count
        elif orm.label == "WRONG_QUANTITY":
            wrong_quantity = orm.count
        elif orm.label == "WRONG_FORM":
            wrong_form = orm.count

    return Summary(
        data=[
            SummaryItem(key="WRONG_DRUG_NAME", label="ผิดชื่อยา", value=wrong_drug_name),
            SummaryItem(key="WRONG_STRENGTH", label="ผิดความแรง", value=wrong_strength),
            SummaryItem(key="WRONG_QUANTITY", label="ผิดจำนวน", value=wrong_quantity),
            SummaryItem(key="WRONG_FORM", label="ผิดรูปแบบ", value=wrong_form),
        ]
    )

def _to_annual_error_summary(rows) -> Summary:
    month_map = {
        (row.month.year, row.month.month): row.count
        for row in rows
    }

    now = datetime.now()
    current_month = now.month
    current_year = now.year

    ordered_months = list(range(current_month + 1, 13)) + list(range(1, current_month + 1))

    data = []

    for m in ordered_months:
        year = current_year if m <= current_month else current_year - 1

        data.append(
            SummaryItem(
                key=f"{year}-{m:02d}",
                label=f"{month_abbr[m]} {year}",
                value=str(month_map.get((year, m), 0))
            )
        )

    return Summary(data=data)
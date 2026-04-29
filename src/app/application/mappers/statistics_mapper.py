from app.application.dto.statistics_dto import DetectionLogDTO, DetectionLogItemDTO
from app.domain.entities.statistics import DetectionLog, DetectionLogItem
from app.application.mappers.detection_mapper import _status_id_to_text

def _to_detection_log_item_dto(log: DetectionLogItem) -> DetectionLogItemDTO:
    return DetectionLogItemDTO(
        detection_id=log.detection_id,
        visit_hn=log.visit_hn,
        visit_vn=log.visit_vn,
        patient_name=log.patient_prefix + log.patient_firstname + " " + log.patient_lastname,
        verified_at=str(log.verified_at),
        status=_status_id_to_text(log.status),
        verified_by=log.employee_firstname + " " + log.employee_lastname if log.employee_firstname is not "" and log.employee_lastname is not "" else ""
    )

def _to_detection_log_dto(detection: DetectionLog) -> DetectionLogDTO:
    return DetectionLogDTO(
        detections=[_to_detection_log_item_dto(log) for log in detection.detections],
        total=detection.total,
        page=detection.page,
        size=detection.size
    )
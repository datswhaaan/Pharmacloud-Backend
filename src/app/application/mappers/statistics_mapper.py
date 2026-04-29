from app.application.dto.statistics_dto import DetectionLogDTO, DetectionLogItemDTO, StatisticsDTO, SummaryDTO
from app.domain.entities.statistics import DetectionLog, DetectionLogItem, Summary

def _to_detection_log_item_dto(log: DetectionLogItem) -> DetectionLogItemDTO:
    return DetectionLogItemDTO(
        detection_id=log.detection_id,
        order_id=log.order_id,
        visit_hn=log.visit_hn,
        visit_vn=log.visit_vn,
        patient_name=log.patient_prefix + log.patient_firstname + " " + log.patient_lastname,
        verified_at=str(log.verified_at),
        verified_by=log.employee_firstname + " " + log.employee_lastname if log.employee_firstname != "" and log.employee_lastname != "" else ""
    )

def _to_detection_log_dto(detection: DetectionLog) -> DetectionLogDTO:
    return DetectionLogDTO(
        detections=[_to_detection_log_item_dto(log) for log in detection.detections],
        total=detection.total,
        page=detection.page,
        size=detection.size
    )

def _to_summary_dto(summary: Summary) -> SummaryDTO:
    return SummaryDTO(
        label=summary.label,
        value=summary.value
    )
    
def _to_statistics_dto(status: Summary, error: Summary, annual: Summary) -> StatisticsDTO:
    return StatisticsDTO(
        status_summary=_to_summary_dto(status),
        error_summary=_to_summary_dto(error),
        annual_error_summary=_to_summary_dto(annual)
    )
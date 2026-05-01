from app.application.dto.statistics_dto import DetectionLogDTO, DetectionLogItemDTO, StatisticsDTO, SummaryDTO
from app.presentation.schemas.statistics_response import DetectionLogResponse, DetectionLogItemResponse, StatisticsResponse, SummaryResponse, SummaryItemResponse

def _to_detection_log_item_response(log: DetectionLogItemDTO) -> DetectionLogItemResponse:
    return DetectionLogItemResponse(
        detection_id=log.detection_id,
        order_id=log.order_id,
        visit_hn=log.visit_hn,
        visit_vn=log.visit_hn,
        patient_name=log.patient_name,
        verified_by=log.verified_by,
        verified_at=log.verified_at
    )

def _to_detection_log_response(detection: DetectionLogDTO) -> DetectionLogResponse:
    return DetectionLogResponse(
        detections=[_to_detection_log_item_response(log) for log in detection.detections],
        total=detection.total,
        page=detection.page,
        size=detection.size
    )

def _to_summary_response(summary: SummaryDTO) -> SummaryResponse:
    return SummaryResponse(
        data=[
            SummaryItemResponse(
                key=si.key,
                label=si.label,
                value=si.value
            ) for si in summary.data
        ])

def _to_statistics_response(statistics: StatisticsDTO) -> StatisticsResponse:
    return StatisticsResponse(
        status_summary=_to_summary_response(statistics.status_summary),
        error_summary=_to_summary_response(statistics.error_summary),
        annual_error_summary=_to_summary_response(statistics.annual_error_summary)
    )
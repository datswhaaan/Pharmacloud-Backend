from app.domain.entities.prescription import OrderDrugItem
from app.domain.repositories.prescription import PrescriptionRepository
from app.application.dto.prescription_dto import PrescriptionDTO, PrescriptionListDTO, DetectionListDTO
from app.application.mappers.prescription_mapper import _to_detection_item_dto, _to_prescription_dto, _to_prescription_list_dto, _to_detection_dto, _to_detection_list_dto

class PrescriptionService:
    def __init__(self, prescription_repository: PrescriptionRepository):
        self.repository = prescription_repository

    def get_by_id(self, id: str) -> PrescriptionDTO:
        prescription = self.repository.get_prescription_by_id(id)
        if prescription is None:
            raise ValueError("Prescription not found")
        return _to_prescription_dto(prescription)
    
    def get_all(
            self, 
            start_time: str, 
            end_time: str, 
            limit: int, skip: int, order: str,
            status: str,
            search: str | None = None
    ) -> PrescriptionListDTO:
        
        match status:
            case "all":
                status_list = []
            case "completed":
                status_list = ["1", "6", "3"]
            case "waiting":
                status_list = ["2", "4"]
            case "cancelled":
                status_list = ["5"]

        prescription_list = self.repository.get_all_prescriptions(start_time, end_time, limit, skip, order, status_list, search)

        if prescription_list is None:
            raise ValueError("Prescriptions not found")
        
        return _to_prescription_list_dto(prescription_list)

    def compare_detections(self, order_id: str) -> DetectionListDTO:
        order_list = self.repository.get_orders_by_order_id(order_id)
        detection_list = self.repository.get_detections_by_order_id(order_id)

        dto = []

        order_map = [order_item.b_item_id for order_item in order_list.orders]
        
        for d in detection_list.detections:
            detection_map = [detection_item.b_item_id for detection_item in d.detections]

            drug_list =[]

            for od in order_map:
                if od in detection_map:
                    drug_list.append(_to_detection_item_dto(order_list.orders[order_map.index(od)], d.detections[order_map.index(od)], "matched"))
                    detection_map.remove(od)

            for dm in detection_map:
                drug_list.append(_to_detection_item_dto(None, d.detections[order_map.index(od)], "extra"))
            
            dto.append(_to_detection_dto(d, drug_list))
            
        return _to_detection_list_dto(order_list, dto)
from app.domain.repositories.detection import DetectionRepository
from app.domain.repositories.prescription import PrescriptionRepository
from app.domain.external.medication_vision_inference import MedicationVisionInferenceService
from app.domain.entities.detection import DetectionList, DetectionItemUpdate
from app.application.dto.detection_dto import DetectionListDTO, DetectionDTO, DetectionInputDTO, DetectionUpdateDTO, DetectionItemUpdateDTO, DetectionItemInputDTO
from app.application.mappers.detection_mapper import _to_detection_item_compare_dto, _to_detection_dto, _to_detection_list_dto, _to_detection_item_input, _to_detection, _to_detection_image, _to_detection_update

class DetectionService:
    def __init__(
        self, 
        detection_repository: DetectionRepository, 
        prescription_repository: PrescriptionRepository, 
        medication_vision_service: MedicationVisionInferenceService
    ):
        self.detection_repo = detection_repository
        self.prescription_repo = prescription_repository
        self.medication_vision = medication_vision_service

    def compare_detections(self, order_id: str) -> DetectionListDTO:
        order_list = self.prescription_repo.get_orders_by_order_id(order_id)
        detection_list = self.detection_repo.get_detections_by_order_id(order_id)

        dto = []

        order_map = [order_item.b_item_id for order_item in order_list.orders]
        
        for d in detection_list.detections:
            detection_map = [detection_item.b_item_id for detection_item in d.detections]

            drug_list =[]

            for od in order_map:
                if od in detection_map:
                    drug_list.append(_to_detection_item_compare_dto(order_list.orders[order_map.index(od)], d.detections[order_map.index(od)], "matched"))
                    detection_map.remove(od)

            for dm in detection_map:
                drug_list.append(_to_detection_item_compare_dto(None, d.detections[order_map.index(od)], "extra"))
            
            dto.append(_to_detection_dto(d, drug_list))
        return _to_detection_list_dto(order_list, dto)
    
    def create_detection(self, detection: DetectionInputDTO, image: bytes) -> DetectionDTO:
        detection_items = self.compare_detection(detection.order_id, detection.detections)
        detection_image = _to_detection_image(image)
        detection = _to_detection(detection.order_id, detection_items)
        
        response = self.detection_repo.create_detection(detection, detection_image)
        return _to_detection_dto(response, response.detections)
    
    def update_detection(self, detection: DetectionUpdateDTO) -> DetectionDTO:
        if detection.status == "ตรวจสอบสำเร็จ":
            drug_list, is_edited = self._update_detection_items(detection.detection_id, detection.drug_list)
            detection_update = _to_detection_update(detection, drug_list, is_edited)
        else:
            detection_update = _to_detection_update(detection, detection.drug_list, False)
            
        response = self.detection_repo.update_detection(detection_update)
        return _to_detection_dto(response, response.detections)

    def compare_detection(self, order_id: str, detection_items: list[DetectionItemInputDTO]) -> DetectionList:
        order_list = self.prescription_repo.get_orders_by_order_id(order_id)
        detection_map = [detection_item.b_item_id for detection_item in detection_items]

        drug_list =[]

        order_map = [order_item.b_item_id for order_item in order_list.orders]

        for od in order_map:
            if od in detection_map:
                drug_list.append(_to_detection_item_input(order_list.orders[order_map.index(od)], detection_items[order_map.index(od)], "MATCHED"))
                detection_map.remove(od)

        for dm in detection_map:
            drug_list.append(_to_detection_item_input(None, detection_items[order_map.index(od)], "EXTRA"))
        
        return drug_list

    def _update_detection_items(
        self,
        detection_id: str,
        detection_items: list[DetectionItemUpdateDTO]
    ):
        detection = self.detection_repo.get_detections_by_detection_id(detection_id)
        is_edited = False

        item_map = {item.detection_item_id: item for item in detection_items}

        for d_item in detection.detections:
            dto = item_map.get(d_item.detection_item_id)
            if not dto:
                continue

            d_item.quantity = dto.quantity

            if dto.is_checked and d_item.match_type == "EXTRA":
                d_item.is_manually_edited = True
                d_item.match_type = "MATCHED"
                is_edited = True

            elif not dto.is_checked and d_item.match_type == "MATCHED":
                d_item.is_manually_edited = True
                d_item.match_type = "EXTRA"
                is_edited = True

        return detection.detections, is_edited
    
    def detection(self, order_id: str, image: bytes) -> DetectionDTO:
        detected_items = self.medication_vision.infer(image)

        detection_image = _to_detection_image(image)
        compared_items = self.compare_detection(order_id, detected_items.detected_items)
        detection = _to_detection(order_id, compared_items)
        response = self.detection_repo.create_detection(
            detection, detection_image
        )
        return _to_detection_dto(response, response.detections)

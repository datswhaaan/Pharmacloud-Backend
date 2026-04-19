from app.domain.repositories.detection import DetectionRepository
from app.domain.repositories.prescription import PrescriptionRepository
from app.domain.entities.detection import Detection, DetectionList, DetectionItem
from app.application.dto.detection_dto import DetectionListDTO, DetectionDTO, DetectionImageInputDTO, DetectionInputDTO
from app.application.mappers.detection_mapper import _to_detection_item_compare_dto, _to_detection_dto, _to_detection_list_dto, _to_detection_item_input, _to_detection, _to_detection_image

class DetectionService:
    def __init__(self, detection_repository: DetectionRepository, prescription_repository: PrescriptionRepository):
        self.detection = detection_repository
        self.prescription = prescription_repository
    
    def compare_detections(self, order_id: str) -> DetectionListDTO:
        order_list = self.prescription.get_orders_by_order_id(order_id)
        detection_list = self.detection.get_detections_by_order_id(order_id)

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
    
    def create_detection(self, detection: DetectionInputDTO, image: DetectionImageInputDTO) -> DetectionDTO:
        detection_items = self.compare_detection(detection)
        detection_image = _to_detection_image(image)
        detection = _to_detection(detection, detection_items)
        
        response = self.detection.create_detection(detection, detection_image)
        return _to_detection_dto(response, response.detections)

    def compare_detection(self, detection: DetectionInputDTO) -> DetectionList:
        detection_items = detection.detections
        order_list = self.prescription.get_orders_by_order_id(detection.order_id)
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
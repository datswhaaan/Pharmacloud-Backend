from app.domain.repositories.prescription import PrescriptionRepository
from app.application.dto.prescription_dto import PrescriptionDTO, PrescriptionListDTO
from app.application.mappers.prescription_mapper import _to_prescription_dto, _to_prescription_list_dto

class PrescriptionService:
    def __init__(self, prescription_repository: PrescriptionRepository):
        self.repository = prescription_repository

    def get_by_id(self, id: str) -> PrescriptionDTO:
        prescription = self.repository.get_prescription_by_id(id)
        if prescription is None:
            raise ValueError("Prescription not found")
        return _to_prescription_dto(prescription)
    
    def get_all(self, start_time: str, end_time: str, limit: int, skip: int, order: str) -> PrescriptionListDTO:
        prescription_list = self.repository.get_all_prescriptions(start_time, end_time, limit, skip, order)
        return _to_prescription_list_dto(prescription_list)
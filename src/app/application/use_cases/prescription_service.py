from app.domain.repositories.prescription import PrescriptionRepository
from app.application.dto.prescription_dto import PrescriptionDTO
from app.application.mappers.prescription_mapper import _to_prescription_dto

class PrescriptionService:
    def __init__(self, prescription_repository: PrescriptionRepository):
        self.repository = prescription_repository

    def get_by_id(self, id: str) -> PrescriptionDTO:
        prescription = self.repository.get_prescription_by_id(id)
        if prescription is None:
            raise ValueError("Prescription not found")
        return _to_prescription_dto(prescription)
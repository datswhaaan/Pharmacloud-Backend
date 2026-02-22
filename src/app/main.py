from fastapi import FastAPI
from app.presentation.routers import drug_metadata, drug

app = FastAPI()
app.include_router(drug_metadata.router)
app.include_router(drug.router)
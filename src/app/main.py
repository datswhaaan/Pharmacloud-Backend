from fastapi import FastAPI
from app.presentation.routers import drug_metadata

app = FastAPI()
app.include_router(drug_metadata.router)
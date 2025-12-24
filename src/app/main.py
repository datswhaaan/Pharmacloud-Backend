from fastapi import FastAPI
from app.presentation.routers import drug

app = FastAPI()
app.include_router(drug.router)
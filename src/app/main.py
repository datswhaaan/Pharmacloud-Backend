from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.routers import drug_metadata, drug, prescription, auth, user, notify, websocket, detection, statistics

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drug_metadata.router)
app.include_router(drug.router)
app.include_router(prescription.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(notify.router)
app.include_router(websocket.router)
app.include_router(detection.router)
app.include_router(statistics.router)
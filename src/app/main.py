from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.routers import drug_metadata, drug, prescription, auth, user

app = FastAPI()

origins = [
    "http://localhost:3000",    # พอร์ตปกติของ Next.js / React
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # อนุญาตตามรายชื่อใน origins
    allow_credentials=True,          # อนุญาตให้ส่ง Cookies หรือ Authentication headers
    allow_methods=["*"],             # อนุญาตทุก HTTP Methods (GET, POST, PUT, etc.)
    allow_headers=["*"],             # อนุญาตทุก Headers
)

app.include_router(drug_metadata.router)
app.include_router(drug.router)
app.include_router(prescription.router)
app.include_router(auth.router)
app.include_router(user.router)
from fastapi import FastAPI
from app.routes import user, auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # hoặc cụ thể ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],   # phải có để chấp nhận OPTIONS
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")

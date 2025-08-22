from fastapi import FastAPI
from app.routes import users, auth, contents, movies, promotions, showtimes, tickets
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
app.include_router(users.router, prefix="/api")
app.include_router(contents.router, prefix="/api")
app.include_router(movies.router, prefix="/api")
app.include_router(promotions.router, prefix="/api")
app.include_router(showtimes.router, prefix="/api")
app.include_router(tickets.router, prefix="/api")
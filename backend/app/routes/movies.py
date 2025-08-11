from fastapi import APIRouter

router = APIRouter()

fake_movies = [
    {
        "id": 1,
        "title": "Avengers: Endgame",
        "cinema": "CGV Vincom",
        "showtimes": ["2025-08-11 18:30", "2025-08-11 21:00"]
    },
    {
        "id": 2,
        "title": "Oppenheimer",
        "cinema": "Lotte Landmark 81",
        "showtimes": ["2025-08-11 19:00", "2025-08-11 22:00"]
    }
]

@router.get("/")
def get_movies():
    return fake_movies

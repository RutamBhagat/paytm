# cors.py
from fastapi.middleware.cors import CORSMiddleware


def get_cors_config():
    origins = ["http://localhost:3000"]
    return CORSMiddleware(
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

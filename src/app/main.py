from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.app.middleware import time_middleware, cors_middleware
from src.app.models import models
from src.app.db.database import engine
from src.app.api import router as api_router


load_dotenv()

app = FastAPI()

# Connect to the database
models.Base.metadata.create_all(bind=engine)

# Middleware
cors_middleware.middleware(app)
app.middleware("http")(time_middleware.middleware)


# Routes
app.include_router(api_router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

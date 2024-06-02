from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.app.models import models
from src.app.db.database import engine
from src.app.api import router as api_router
from src.app.middleware.cors_middleware import add_cors_middleware


load_dotenv()

app = FastAPI()

# Connect to the database
models.Base.metadata.create_all(bind=engine)

# Middleware
add_cors_middleware(app)

# Routes
app.include_router(api_router)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

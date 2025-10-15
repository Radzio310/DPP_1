from fastapi import FastAPI
from .movies import router as movies_router
from .links import router as links_router
from .ratings import router as ratings_router
from .tags import router as tags_router

app = FastAPI()

app.include_router(movies_router)
app.include_router(links_router)
app.include_router(ratings_router)
app.include_router(tags_router)

@app.get("/")
def read_root():
    return {"hello": "world"}
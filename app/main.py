import uvicorn
from fastapi import FastAPI
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# import models
# from database import engine
# from config import settings
# models.Base.metadata.create_all(bind=engine)
# # don't need auto update tables
# # using sqlalchemy (not good) because
# # we have alembic

app = FastAPI()
# app = FastAPI(title='slow API',
#               docs_url='/docs',
#               redoc_url='/redoc',
#               openapi_url='/openapi.json')
origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # HTTP methods allowed
    allow_headers=["*"],  # HTTP headers allowed
)
# middlewares are fuctions run before every requests

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message : Hello World Root"}


if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True,
    #             debug=True, workers=3)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=5)

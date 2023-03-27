import uvicorn
from fastapi import FastAPI

import models
from database import engine
from routers import post, user, auth, vote
from config import settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message : Hello World Root"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True,
                debug=True, workers=3)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=5)

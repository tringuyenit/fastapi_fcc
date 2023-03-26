import time

import psycopg2
import uvicorn
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

import models
from database import engine

from routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost",
                                database="fastapi",
                                user="postgres",
                                password="meomeo",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected sucessfully")
        break
    except Exception as e:
        print("DB connect failed")
        print("error:", e)
        time.sleep(2)


@app.get("/")
def root():
    return {"message : Hello World Root"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True,
    #             debug=True, workers=3)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=5)
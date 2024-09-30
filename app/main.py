from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, posts, auth, votes

app = FastAPI()

origins = [
    "*" # All domains are not blocked
    # "https://www.google.com",
    # "https://www.youtube.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


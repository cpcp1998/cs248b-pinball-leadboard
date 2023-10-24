from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://preview.openprocessing.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convert_record(record):
    return {"user": record.user, "score": record.score}


@app.get("/v1/{game_id}/get/", response_model=schemas.ScoreRecord)
def get_single(game_id: int, user: str, db: Session = Depends(get_db)):
    record = crud.get_single(db, game_id=game_id, user=user)
    if record:
        return convert_record(record)
    return {"user": user, "score": None}


@app.get("/v1/{game_id}/leaderboard/", response_model=List[schemas.ScoreRecord])
def leaderboard(game_id: int, limit: int = 10, db: Session = Depends(get_db)):
    limit = min(limit, 100)
    leaderboard = crud.get_top(db, game_id=game_id, limit=limit)
    return [convert_record(r) for r in leaderboard]


@app.post("/v1/{game_id}/update/", response_model=schemas.ScoreRecord)
def update_single(game_id: int, body: schemas.ScoreRecord, db: Session = Depends(get_db)):
    record = crud.update_single(db, game_id=game_id, user=body.user, score=body.score)
    return convert_record(record)


@app.post("/v1/{game_id}/delete/")
def delete_single(game_id: int, user: str, db: Session = Depends(get_db)):
    crud.delete_single(db, game_id, user)

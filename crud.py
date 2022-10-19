from sqlalchemy.orm import Session

from . import models, schemas


def get_single(db: Session, game_id: int, user: str):
    return (db.query(models.HighScore)
        .filter(models.HighScore.game_id == game_id)
        .filter(models.HighScore.user == user)
        .first())


def get_top(db: Session, game_id: int, limit: int = 10):
    return (db.query(models.HighScore)
        .filter(models.HighScore.game_id == game_id)
        .order_by(models.HighScore.score.desc(), models.HighScore.ts)
        .limit(limit)
        .all())


def update_single(db: Session, game_id: int, user: str, score: float):
    record = get_single(db, game_id, user)
    if record:
        if score is not None and score == score and score > record.score:
            record.score = score
    else:
        record = models.HighScore(game_id=game_id, user=user, score=score)
        db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_single(db: Session, game_id: int, user: str):
    (db.query(models.HighScore)
        .filter(models.HighScore.game_id == game_id)
        .filter(models.HighScore.user == user)
        .delete())
    db.commit()

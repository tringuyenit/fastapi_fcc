from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app import schemas, utils, models
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} is not found")
    return user

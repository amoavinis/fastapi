from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db.database import get_db
from ..utils.password import hash_password, verify_password
from ..utils.jwt import create_access_token
from ..utils.auth import get_current_user, get_current_admin_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    # Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user.username}' is already taken"
        )

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create user with hashed password
    user_data = user.model_dump()
    user_data['password'] = hashed_password

    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[schemas.User])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.User)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found."
        )

    return user

@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Find user by username
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    # Check if user exists and password is correct
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with user data
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}


from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from typing import Optional


def get_user_by_email(db: Session, correo: str) -> Optional[User]:
	return db.query(User).filter(User.correo == correo).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
	return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
	hashed_password = get_password_hash(user_in.password)
	db_user = User(
		nombre=user_in.nombre,
		correo=user_in.correo,
		password_hash=hashed_password,
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


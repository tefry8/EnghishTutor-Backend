
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.crud_users import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token
from app.models.user import User
from typing import Optional


def register_user(db: Session, user_in: UserCreate) -> User:
	"""Registra un nuevo usuario si el correo no existe."""
	existing_user = get_user_by_email(db, user_in.correo)
	if existing_user:
		raise ValueError("El correo ya está registrado")
	return create_user(db, user_in)


def authenticate_user(db: Session, correo: str, password: str) -> Optional[User]:
	"""Autentica un usuario por correo y contraseña."""
	user = get_user_by_email(db, correo)
	if not user:
		return None
	if not verify_password(password, user.password_hash):
		return None
	return user


def generate_access_token(user: User) -> str:
	"""Genera un token JWT para el usuario autenticado."""
	data = {"sub": str(user.id), "correo": user.correo}
	return create_access_token(data)

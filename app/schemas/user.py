
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
	nombre: str
	correo: EmailStr


class UserCreate(UserBase):
	password: str


class UserLogin(BaseModel):
	correo: EmailStr
	password: str


class UserOut(UserBase):
	id: int
	fecha_registro: Optional[datetime]

	class Config:
		from_attributes = True

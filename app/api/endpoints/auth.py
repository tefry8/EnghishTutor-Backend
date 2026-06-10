
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_services import register_user, authenticate_user, generate_access_token
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
	try:
		user = register_user(db, user_in)
		return user
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
	user = authenticate_user(db, user_in.correo, user_in.password)
	if not user:
		raise HTTPException(status_code=401, detail="Credenciales incorrectas")
	access_token = generate_access_token(user)
	return {"access_token": access_token, "token_type": "bearer"}

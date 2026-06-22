
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_services import register_user, authenticate_user, generate_access_token
from app.db.session import get_db
from app.core.security import decode_access_token
from app.crud.crud_users import get_user_by_id

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

@router.get("/me", response_model=UserOut)
def me(authorization: str = Header(None), db: Session = Depends(get_db)):
	if not authorization:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta el encabezado Authorization")
	parts = authorization.split()
	if len(parts) != 2 or parts[0].lower() != "bearer":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Encabezado Authorization inválido")
	token = parts[1]
	payload = decode_access_token(token)
	if not payload:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
	sub = payload.get("sub")
	if not sub:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sin sujeto")
	try:
		user_id = int(sub)
	except (TypeError, ValueError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ID de usuario inválido en token")
	user = get_user_by_id(db, user_id)
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
	return user

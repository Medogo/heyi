from fastapi import APIRouter, Depends, HTTPException
from app.services.linkedin_service import linkedin_service
from app.db.session import SessionLocal
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurIn, UtilisateurOut
import datetime
from app.core.config import settings

router = APIRouter()

@router.post("/register")
def register(utilisateur: UtilisateurIn):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter_by(email=utilisateur.email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            user = Utilisateur(
                nom=utilisateur.nom,
                prenom=utilisateur.prenom,
                email=utilisateur.email,
                password=utilisateur.password,
                active=utilisateur.active,
                date_creation=datetime.datetime.now(),
                date_modification=datetime.datetime.now(),
                access_token=utilisateur.access_token,
                refresh_token=utilisateur.refresh_token
            )
            db.add(user)
            db.commit()
            return user

@router.get("/login")
def login(email: str, password: str):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter_by(email=email).first()
        if user and user.password == password:
            access_token = jwt.encode({"id": user.id}, settings.SECRET_KEY, algorithm="HS256")
            return {"access_token": access_token}
        else:   
            raise HTTPException(status_code=400, detail="Invalid email or password")

@router.get("/refresh_token")
def refresh_token(refresh_token: str):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter_by(refresh_token=refresh_token).first()
        if user:
            access_token = jwt.encode({"id": user.id}, settings.SECRET_KEY, algorithm="HS256")
            return {"access_token": access_token}
        else:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

@router.get("/logout")
def logout(access_token: str):
    return {"message": "Logout"}
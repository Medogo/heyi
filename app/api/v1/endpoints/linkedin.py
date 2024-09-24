from fastapi import APIRouter, Depends, HTTPException
from app.services.linkedin_service import linkedin_service

from app.db.session import SessionLocal
from app.models.utilisateur import Utilisateur

router = APIRouter()

@router.get("/auth")
async def linkedin_auth():
    auth_url = linkedin_service.get_authorization_url()
    return {"auth_url": auth_url}

@router.get('/authorization_url')
def get_authorization_url():
    return linkedin_service.get_authorization_url()
"""

@router.get("/callback")
async def linkedin_callback(code: str):
    try:
        tokens = linkedin_service.get_access_token(code)
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))"""



"""
@router.get("/callback")
async def linkedin_callback(code: str):
    try:
        tokens = linkedin_service.get_access_token(code)
        return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))"""


@router.get('/access_token')
def get_access_token(code: str):
    return linkedin_service.get_access_token(code)

@router.get('/refresh_access_token')
def refresh_access_token():
    return linkedin_service.refresh_access_token()

@router.get('/profile')
def get_profile(access_token: str):
    return linkedin_service.get_profile(access_token)

@router.patch('/profile')
def update_profile(profile_data: dict, access_token: str):
    return linkedin_service.update_profile(profile_data)

@router.get('/connections')
def get_connections(access_token: str):
    return linkedin_service.get_connections(access_token)

@router.get('/job')
def get_job(access_token: str):
    return linkedin_service.get_job(access_token)

@router.get('/callback')
def callback(code: str):
    return linkedin_service.get_access_token(code)



@router.get("/tokens")
async def get_tokens(user_email: str):
    with SessionLocal() as db:
        user = db.query(Utilisateur).filter_by(email=user_email).first()
        if user:
            return {
                "access_token": user.access_token,
                "refresh_token": user.refresh_token
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")
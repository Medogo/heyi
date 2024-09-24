import requests
from fastapi import HTTPException
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.utilisateur import Utilisateur
"""
from app.models.linkedin import Linkedin
from app.models.linkedin import LinkedinProfile
from app.models.linkedin import LinkedinConnection
from app.models.linkedin import LinkedinJob
from app.models.linkedin import LinkedinCompany
from app.models.linkedin import LinkedinEducation
from app.models.linkedin import LinkedinExperience
from app.models.linkedin import LinkedinInterest
from app.models.linkedin import LinkedinPublication
from app.models.linkedin import LinkedinSkill"""

class LinkedinService:
    def get_authorization_url(self):
        params = {
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "response_type": "code",
            "scope": "w_member_social",
        }
        return "https://www.linkedin.com/oauth/v2/authorization?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    """def get_access_token(self, code):
        params = {
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "grant_type": "authorization_code",
            "code": code,
        }
        response = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data=params)
        if response.status_code == 200 and "access_token" in response.json():
            token = response.json()["access_token"]
            print(f"Access Token: {token}")
            return response.json()
        else:
            raise HTTPException(status_code=400, detail="Something went wrong")"""
    

    def get_access_token(self, code):
        params = {
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "grant_type": "authorization_code",
            "code": code,
        }
        response = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data=params)
        if response.status_code == 200 and "access_token" in response.json():
            tokens = response.json()
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]

            # Enregistrer les jetons dans la base de données
            with SessionLocal() as db:
                user = db.query(Utilisateur).filter_by(email=email).first()
                user.access_token = access_token
                user.refresh_token = refresh_token
                db.commit()

            return tokens
        else:
            raise HTTPException(status_code=400, detail="Something went wrong")
            
    def refresh_access_token(self):
        params = {
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "grant_type": "refresh_token",
            "refresh_token": settings.LINKEDIN_REFRESH_TOKEN,
        }
        response = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data=params)
        if response.status_code == 200:
            token = response.json()
            settings.LINKEDIN_ACCESS_TOKEN = token["access_token"]
            return token
        else:
            raise HTTPException(status_code=400, detail="Something went wrong")
    

    
    def get_profile(self, access_token):
        params = {
            "projection": "(id,firstName,lastName,profilePicture(displayImage~:playableStreams))",
            "fields": "id,firstName,lastName,profilePicture(displayImage~:playableStreams)",
        }
        response = requests.get("https://api.linkedin.com/v2/me", headers={"Authorization": f"Bearer {access_token}"}, params=params)
        return response.json()
    

    def update_profile(self, profile_data):
        headers = {
            "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.patch(
            "https://api.linkedin.com/v2/me",
            headers=headers,
            json=profile_data
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=400, detail=f"Error updating profile: {response.text}")

    
    def get_connections(self, access_token):
        params = {
            "projection": "(id,firstName,lastName,profilePicture(displayImage~:playableStreams))",
            "fields": "id,firstName,lastName,profilePicture(displayImage~:playableStreams)",
        }
        response = requests.get("https://api.linkedin.com/v2/me/connections", headers={"Authorization": f"Bearer {access_token}"}, params=params)
        return response.json()
    
    def get_job(self, access_token):
        params = {
            "projection": "(id,title,company(name,id),summary,positions(id,title,summary,startDate,endDate))",
            "fields": "id,title,company(name,id),summary,positions(id,title,summary,startDate,endDate)",
        }
        response = requests.get("https://api.linkedin.com/v2/me/job-bookmarks", headers={"Authorization": f"Bearer {access_token}"}, params=params)
        return response.json()


linkedin_service = LinkedinService()
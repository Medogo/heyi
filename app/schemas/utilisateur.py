from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str
    active: bool
    date_creation: datetime
    date_modification: datetime
    access_token: str
    refresh_token: str

class UtilisateurIn(UtilisateurBase):
    password: str

class UtilisateurOut(UtilisateurBase):
    id: int
    date_creation: str
    date_modification: Optional[datetime] = None

    class Config:
        orm_mode = True
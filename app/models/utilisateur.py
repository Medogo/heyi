from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship



class Utilisateur(Base):
    __tablename__ = 'utilisateur'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50))
    prenom = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    active = Column(Boolean)
    access_token = Column(String)
    refresh_token = Column(String)
    date_creation = Column(DateTime)
    date_modification = Column(DateTime)

    """def __init__(self, nom, prenom, email, password, active, date_creation, date_modification):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = password
        self.active = active
        self.date_creation = date_creation
        self.date_modification = date_modification  """
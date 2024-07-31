from sqlalchemy import Column, Integer,String,Boolean
from database.database import Base

from typing import Any

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True)
    password = Column(String)
    isactive =Column(Boolean,default=True)

    @classmethod
    def get_user_by_username(cls, db_session: Any, username: str):
        return db_session.query(cls).filter(cls.username == username).first()
    
    @classmethod
    def get_all_user(cls,db_session:Any):
        return db_session.query(cls).all()
    
    @classmethod
    def create_user(cls,db_session:Any,data):
        user = cls(**data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return True,user
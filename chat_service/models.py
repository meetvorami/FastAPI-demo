from database.database import Base
from sqlalchemy import Column,String,ForeignKey, Integer, DateTime,desc
from sqlalchemy.orm import relationship
from datetime import datetime


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer,primary_key=True)
    room_name = Column(String,unique=True)
    
    
    message = relationship("Message", back_populates="room")
    room_user = relationship("RoomUser", back_populates="room")
                             
class RoomUser(Base):
    __tablename__ = "roomuser"
    id = Column(Integer,primary_key=True)
    room_id = Column(Integer,ForeignKey("room.id"))
    user_id = Column(Integer,ForeignKey("users.id"))
    
    user = relationship("Users", back_populates="rooms")
    room = relationship("Room", back_populates="room_user")
    



class Message(Base):
    __tablename__ = "message"
    
    id = Column(Integer,primary_key=True)
    room_id = Column(Integer,ForeignKey("room.id"))
    message = Column(String,nullable=False)
    created_by = Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime,default=datetime.now())
    
    room = relationship("Room", back_populates="message")
    created_by_user = relationship("Users", back_populates="messages")
    
    def to_dict(self):
        return {
            "id": self.id,
            "room_id":self.room_id,
            "message": self.message,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat()
        }

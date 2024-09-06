from database.database import get_db
from chat_service.models import Message, RoomUser
from sqlalchemy import  func 

class UserServices:
    def __init__(self) -> None:
        self.db = next(get_db())
    
    def check_if_user_part_of_room(self,user_id):
        data = self.db.query(RoomUser.id).filter(RoomUser.user_id == user_id)
        return [id[0] for id in data]

    def get_latest_message(self,room_list, skip:int,limit:int):
        subquery = (
                self.db.query(
                    Message.room_id,
                    func.max(Message.created_at).label('latest_timestamp')
                )
                .filter(Message.room_id.in_(room_list))
                .group_by(Message.room_id)
                .subquery()
            )


        # Join the subquery with the original Message table to get full message details
        data = (
        self.db.query(Message)
            .join(
                subquery,
                (Message.room_id == subquery.c.room_id) &
                (Message.created_at == subquery.c.latest_timestamp)
            )
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        
        data =  [value.to_dict() for value in data ]
        return data
        
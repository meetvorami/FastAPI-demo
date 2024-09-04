from sqlalchemy import Column, Float, ForeignKey, Integer, String

from database.database import Base


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String)
    price = Column(Float)

    @classmethod
    def check_product_if_already_exist(cls, db_session, name, user_id):
        return (
            db_session.query(cls)
            .filter(cls.user_id == user_id, cls.name == name)
            .first()
        )

    @classmethod
    def create_product(cls, db_session, data):
        product = Products(**data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        return product

    @classmethod
    def get_all_product_from_user_id(cls, db_session, user_id, skip, limit):
        return (
            db_session.query(cls)
            .filter(cls.user_id == user_id)
            .limit(limit)
            .offset(skip)
            .all()
        )

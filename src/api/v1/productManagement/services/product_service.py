from fastapi import HTTPException

from database.database import get_db
from src.api.v1.productManagement.models.product_model import Products


class ProductService:
    def __init__(self, user_id) -> None:
        self.db = next(get_db())
        self.user_id = user_id

    def create_product(self, product):
        check_product = Products.check_product_if_already_exist(
            self.db, product.name, self.user_id
        )
        if check_product:
            raise HTTPException(
                status_code=400, detail="product with that name already exist"
            )

        data = product.dict()
        data["user_id"] = self.user_id
        return Products.create_product(self.db, data)
        
    def get_all_products(self,skip,limit):
        return Products.get_all_product_from_user_id(self.db, self.user_id,skip,limit)

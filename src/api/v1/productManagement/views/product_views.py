from src.api.v1.productManagement.schema.product_schema import ProductSchema
from fastapi import APIRouter,Depends
from src.api.v1.common_utils.auth_utils import get_current_user
from src.api.v1.productManagement.services.product_service import ProductService

product_router = APIRouter(prefix="/product",tags=["Products Management"])


@product_router.post("/create_product")
def create_product(product:ProductSchema,user=Depends(get_current_user)):
    return ProductService(user.id).create_product(product)
     

@product_router.post("/list_all_products")
def list_all_products(limit:int=10,skip:int=0,user=Depends(get_current_user)):
    return ProductService(user.id).get_all_products(skip,limit)
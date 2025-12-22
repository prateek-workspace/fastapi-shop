from pydantic import BaseModel
from typing import List
from decimal import Decimal


class AddToCartIn(BaseModel):
    product_id: int
    variant_id: int
    quantity: int = 1


class UpdateCartItemIn(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    product_id: int
    variant_id: int
    quantity: int
    price: Decimal
    total: Decimal


class CartOut(BaseModel):
    items: List[CartItemOut]
    total_amount: Decimal

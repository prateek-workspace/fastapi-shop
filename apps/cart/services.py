from decimal import Decimal

from apps.cart.models import Cart, CartItem
from apps.products.models import ProductVariant
from apps.orders.services import OrderService
from config.database import SessionLocal


class CartService:

    @staticmethod
    def _get_or_create_cart(user_id: int):
        cart = Cart.filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart.create(user_id=user_id)
        return cart

    @staticmethod
    def add_item(user_id: int, data: dict):
        cart = CartService._get_or_create_cart(user_id)

        with SessionLocal() as session:
            item = (
                session.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id,
                    CartItem.variant_id == data["variant_id"]
                )
                .first()
            )

            if item:
                item.quantity += data["quantity"]
            else:
                session.add(
                    CartItem(
                        cart_id=cart.id,
                        product_id=data["product_id"],
                        variant_id=data["variant_id"],
                        quantity=data["quantity"]
                    )
                )

            session.commit()

        return CartService.get_cart(user_id)

    @staticmethod
    def get_cart(user_id: int):
        cart = Cart.filter(Cart.user_id == user_id).first()
        if not cart:
            return {"items": [], "total_amount": Decimal("0.00")}

        items = []
        total = Decimal("0.00")

        for item in cart.items:
            variant = ProductVariant.get_or_404(item.variant_id)
            item_total = variant.price * item.quantity
            total += item_total

            items.append({
                "id": item.id,
                "product_id": item.product_id,
                "variant_id": item.variant_id,
                "quantity": item.quantity,
                "price": variant.price,
                "total": item_total
            })

        return {"items": items, "total_amount": total}

    @staticmethod
    def update_item(user_id: int, item_id: int, quantity: int):
        item = CartItem.get_or_404(item_id)
        item.quantity = quantity
        item.save()
        return CartService.get_cart(user_id)

    @staticmethod
    def delete_item(user_id: int, item_id: int):
        CartItem.delete(item_id)
        return CartService.get_cart(user_id)

    @staticmethod
    def checkout(user_id: int, address_id: int):
        cart = Cart.filter(Cart.user_id == user_id).first()
        if not cart or not cart.items:
            raise ValueError("Cart is empty")

        order_data = {
            "address_id": address_id,
            "items": [
                {
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity
                }
                for item in cart.items
            ]
        }

        order = OrderService.create_order(user_id, order_data)

        # Clear cart
        CartItem.filter(CartItem.cart_id == cart.id).delete()

        return order

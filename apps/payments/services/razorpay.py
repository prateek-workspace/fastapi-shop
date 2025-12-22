import razorpay
from config.settings import AppConfig

class RazorpayGateway:
    def __init__(self):
        config = AppConfig.get_config()
        self.client = razorpay.Client(
            auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET)
        )

    def create_payment(self, order):
        return self.client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": order.currency,
            "receipt": f"order_{order.id}",
            "payment_capture": 1
        })

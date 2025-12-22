from config.settings import AppConfig
from .mock import MockPaymentGateway
from .razorpay import RazorpayGateway

def get_payment_gateway():
    config = AppConfig.get_config()

    if config.PAYMENT_MODE == "razorpay":
        return RazorpayGateway()

    return MockPaymentGateway()

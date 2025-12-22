from .base import PaymentGateway

class MockPaymentGateway(PaymentGateway):

    def create_payment(self, order):
        return {
            "status": "success",
            "payment_id": f"mock_{order.id}",
            "amount": order.total_amount,
            "currency": order.currency
        }

    def verify_payment(self, payload):
        return True

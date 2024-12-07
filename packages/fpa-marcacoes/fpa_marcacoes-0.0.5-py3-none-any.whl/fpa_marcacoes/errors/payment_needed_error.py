from ..core.api_error import ApiError

class PaymentNeededError(ApiError):
    def __init__(self, body):
        super().__init__(status_code=402, body = body)
import uuid
from dataclasses import dataclass
from enum import Enum
from payments import db_query


class PaymentStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class SuccessCreatePayment:
    uuid: str
    url_for_payment: str
    status: PaymentStatus


@dataclass
class Payment:
    uuid: str
    status: PaymentStatus | str
    user_id: int
    amount: float

    @staticmethod
    async def create_payment(user_id, amount):
        u = str(uuid.uuid4())
        await db_query.create_payment(u, PaymentStatus.PENDING.value, user_id, amount)
        return Payment(u, PaymentStatus.PENDING, user_id, amount)

    @staticmethod
    async def get_payment(order_id: str):
        return Payment(*await db_query.get_payment(order_id))

    async def complete_payment(self):
        await db_query.edit_payment_status(self.uuid, PaymentStatus.COMPLETED.value)

from pydantic import BaseModel
from typing import Literal

OrderStatus = Literal["pending", "processing", "dispatched", "delivered", "cancelled"]


class UpdateOrderStatus(BaseModel):
    status: OrderStatus

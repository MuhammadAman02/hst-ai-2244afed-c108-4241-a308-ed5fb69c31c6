from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    id: Optional[int] = None
    amount: float
    sender: str
    recipient: str
    timestamp: datetime
    is_fraudulent: Optional[bool] = False
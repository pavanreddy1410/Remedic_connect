from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    user_id: str
    approved: bool

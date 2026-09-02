from datetime import date
from typing import Optional

from pydantic import BaseModel


class LeaveCreate(BaseModel):

    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveResponse(BaseModel):

    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str]
    status: str

    class Config:
        from_attributes = True
from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class AttendanceResponse(BaseModel):

    id: int
    employee_id: int
    attendance_date: date
    check_in: time
    check_out: Optional[time]
    status: str

    class Config:
        from_attributes = True
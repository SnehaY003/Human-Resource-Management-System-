from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):

    employee_code: str = Field(
        min_length=2,
        max_length=20
    )

    first_name: str = Field(
        min_length=1,
        max_length=50
    )

    last_name: str = Field(
        min_length=1,
        max_length=50
    )

    email: EmailStr

    phone: str = Field(
        min_length=10,
        max_length=15
    )

    gender: Optional[str] = None

    dob: Optional[date] = None

    joining_date: date

    salary: float = Field(
        gt=0
    )

    designation: str

    department_id: int

    status: str = "active"


class EmployeeUpdate(BaseModel):

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    joining_date: Optional[date] = None
    salary: Optional[float] = Field(
        default=None,
        gt=0
    )
    designation: Optional[str] = None
    department_id: Optional[int] = None
    status: Optional[str] = None


class EmployeeResponse(BaseModel):

    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: Optional[str]
    dob: Optional[date]
    joining_date: date
    salary: float
    designation: str
    department_id: int
    status: str

    class Config:
        from_attributes = True
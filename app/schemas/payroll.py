from pydantic import BaseModel, Field


class PayrollCreate(BaseModel):

    employee_id: int

    month: str

    basic_salary: float = Field(gt=0)

    bonus: float = Field(
        default=0,
        ge=0
    )

    deduction: float = Field(
        default=0,
        ge=0
    )


class PayrollResponse(BaseModel):

    id: int
    employee_id: int
    month: str
    basic_salary: float
    bonus: float
    deduction: float
    net_salary: float

    class Config:
        from_attributes = True
from typing import Optional
from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    department_name: str = Field(
        min_length=2,
        max_length=100
    )

    manager_name: Optional[str] = None

    description: Optional[str] = None


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    manager_name: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(BaseModel):
    id: int
    department_name: str
    manager_name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
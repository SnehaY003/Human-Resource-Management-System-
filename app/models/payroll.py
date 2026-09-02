from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from app.database import Base


class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    month = Column(
        String(7),
        nullable=False
    )

    basic_salary = Column(
        Float,
        nullable=False
    )

    bonus = Column(
        Float,
        default=0
    )

    deduction = Column(
        Float,
        default=0
    )

    net_salary = Column(
        Float,
        nullable=False
    )
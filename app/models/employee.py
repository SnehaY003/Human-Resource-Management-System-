from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey
)

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    phone = Column(
        String(15),
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=True
    )

    dob = Column(
        Date,
        nullable=True
    )

    joining_date = Column(
        Date,
        nullable=False
    )

    salary = Column(
        Float,
        nullable=False
    )

    designation = Column(
        String(100),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    status = Column(
        String(20),
        default="active",
        nullable=False
    )
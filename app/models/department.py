from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    department_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    manager_name = Column(
        String(100),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )
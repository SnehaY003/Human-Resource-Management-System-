from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.payroll import Payroll
from app.models.employee import Employee

from app.schemas.payroll import (
    PayrollCreate,
    PayrollResponse
)

from app.dependencies.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/payroll",
    tags=["Payroll"]
)


@router.post(
    "",
    response_model=PayrollResponse
)
def create_payroll(
    data: PayrollCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    employee = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    net_salary = (
        data.basic_salary
        + data.bonus
        - data.deduction
    )

    payroll = Payroll(
        employee_id=data.employee_id,
        month=data.month,
        basic_salary=data.basic_salary,
        bonus=data.bonus,
        deduction=data.deduction,
        net_salary=net_salary
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return payroll


@router.get(
    "",
    response_model=list[PayrollResponse]
)
def get_payroll(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Payroll).all()


@router.get(
    "/{employee_id}",
    response_model=list[PayrollResponse]
)
def get_employee_payroll(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Payroll).filter(
        Payroll.employee_id == employee_id
    ).all()
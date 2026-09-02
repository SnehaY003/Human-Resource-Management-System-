from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.leave import Leave
from app.models.payroll import Payroll

from app.dependencies.auth import admin_required


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/employees")
def employee_report(
    department_id: int | None = None,
    employee_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    query = db.query(Employee)

    if department_id:
        query = query.filter(
            Employee.department_id == department_id
        )

    if employee_id:
        query = query.filter(
            Employee.id == employee_id
        )

    return query.all()


@router.get("/attendance")
def attendance_report(
    employee_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    query = db.query(Attendance)

    if employee_id:
        query = query.filter(
            Attendance.employee_id == employee_id
        )

    return query.all()


@router.get("/leaves")
def leave_report(
    employee_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    query = db.query(Leave)

    if employee_id:
        query = query.filter(
            Leave.employee_id == employee_id
        )

    return query.all()


@router.get("/payroll")
def payroll_report(
    employee_id: int | None = None,
    month: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    query = db.query(Payroll)

    if employee_id:
        query = query.filter(
            Payroll.employee_id == employee_id
        )

    if month:
        query = query.filter(
            Payroll.month == month
        )

    return query.all()
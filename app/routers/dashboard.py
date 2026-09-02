from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.employee import Employee
from app.models.department import Department
from app.models.attendance import Attendance
from app.models.leave import Leave
from app.models.payroll import Payroll

from app.dependencies.auth import admin_required


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    total_employees = db.query(
        func.count(Employee.id)
    ).scalar()

    active_employees = db.query(
        func.count(Employee.id)
    ).filter(
        Employee.status == "active"
    ).scalar()

    departments = db.query(
        func.count(Department.id)
    ).scalar()

    today_attendance = db.query(
        func.count(Attendance.id)
    ).filter(
        Attendance.attendance_date == date.today()
    ).scalar()

    pending_leaves = db.query(
        func.count(Leave.id)
    ).filter(
        Leave.status == "Pending"
    ).scalar()

    monthly_payroll = db.query(
        func.coalesce(
            func.sum(Payroll.net_salary),
            0
        )
    ).filter(
        Payroll.month == date.today().strftime("%Y-%m")
    ).scalar()

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "departments": departments,
        "today_attendance": today_attendance,
        "pending_leaves": pending_leaves,
        "monthly_payroll": monthly_payroll
    }
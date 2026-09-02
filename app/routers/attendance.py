from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceResponse

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post(
    "/check-in",
    response_model=AttendanceResponse
)
def check_in(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    today = date.today()

    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for today"
        )

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=today,
        check_in=datetime.now().time(),
        status="Present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


@router.put(
    "/check-out",
    response_model=AttendanceResponse
)
def check_out(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    today = date.today()

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Check-in not found for today"
        )

    if attendance.check_out:
        raise HTTPException(
            status_code=400,
            detail="Already checked out"
        )

    current_time = datetime.now().time()

    if current_time <= attendance.check_in:
        raise HTTPException(
            status_code=400,
            detail="Check-out cannot be before check-in"
        )

    attendance.check_out = current_time

    db.commit()
    db.refresh(attendance)

    return attendance


@router.get(
    "",
    response_model=list[AttendanceResponse]
)
def get_attendance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Attendance).all()


@router.get(
    "/{employee_id}",
    response_model=list[AttendanceResponse]
)
def get_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()
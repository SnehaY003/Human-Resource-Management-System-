from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.leave import Leave
from app.models.employee import Employee

from app.schemas.leave import (
    LeaveCreate,
    LeaveResponse
)

from app.dependencies.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/leave",
    tags=["Leave Management"]
)


@router.post(
    "/apply",
    response_model=LeaveResponse
)
def apply_leave(
    data: LeaveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    employee = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    overlapping = db.query(Leave).filter(
        Leave.employee_id == data.employee_id,
        Leave.status != "Rejected",
        Leave.start_date <= data.end_date,
        Leave.end_date >= data.start_date
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Leave dates overlap with existing leave"
        )

    leave = Leave(
        employee_id=data.employee_id,
        leave_type=data.leave_type,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="Pending"
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave


@router.get(
    "",
    response_model=list[LeaveResponse]
)
def get_leaves(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Leave).all()


@router.put(
    "/{leave_id}/approve",
    response_model=LeaveResponse
)
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    leave.status = "Approved"

    db.commit()
    db.refresh(leave)

    return leave


@router.put(
    "/{leave_id}/reject",
    response_model=LeaveResponse
)
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    leave.status = "Rejected"

    db.commit()
    db.refresh(leave)

    return leave
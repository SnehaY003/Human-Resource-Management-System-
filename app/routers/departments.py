from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.department import Department

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)

from app.dependencies.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    response_model=DepartmentResponse
)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    existing = db.query(Department).filter(
        Department.department_name ==
        data.department_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Department already exists"
        )

    department = Department(
        department_name=data.department_name,
        manager_name=data.manager_name,
        description=data.description
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def get_departments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Department).all()


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    if data.department_name:

        duplicate = db.query(Department).filter(
            Department.department_name ==
            data.department_name,
            Department.id != department_id
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Department name already exists"
            )

        department.department_name = (
            data.department_name
        )

    if data.manager_name is not None:
        department.manager_name = data.manager_name

    if data.description is not None:
        department.description = data.description

    db.commit()
    db.refresh(department)

    return department


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }
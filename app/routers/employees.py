from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.employee import Employee
from app.models.department import Department

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)

from app.dependencies.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "",
    response_model=EmployeeResponse
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    existing_email = db.query(Employee).filter(
        Employee.email == data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )

    existing_code = db.query(Employee).filter(
        Employee.employee_code ==
        data.employee_code
    ).first()

    if existing_code:
        raise HTTPException(
            status_code=409,
            detail="Employee code already exists"
        )

    department = db.query(Department).filter(
        Department.id == data.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    employee = Employee(**data.model_dump())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def get_employees(
    search: str | None = None,
    department_id: int | None = None,
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    query = db.query(Employee)

    if search:
        query = query.filter(
            (Employee.first_name.ilike(
                f"%{search}%"
            )) |
            (Employee.last_name.ilike(
                f"%{search}%"
            ))
        )

    if department_id:
        query = query.filter(
            Employee.department_id ==
            department_id
        )

    if status:
        query = query.filter(
            Employee.status == status
        )

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
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

    return employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "department_id" in update_data:

        department = db.query(
            Department
        ).filter(
            Department.id ==
            update_data["department_id"]
        ).first()

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }
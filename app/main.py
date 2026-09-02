from fastapi import FastAPI

from app.database import Base, engine

from app.models import (
    User,
    Department,
    Employee,
    Attendance,
    Leave,
    Payroll
)

from app.routers import (
    auth,
    departments,
    employees,
    attendance,
    leave,
    payroll,
    dashboard,
    reports
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Human Resource Management System",
    description="HRMS Backend API",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(departments.router)
app.include_router(employees.router)
app.include_router(attendance.router)
app.include_router(leave.router)
app.include_router(payroll.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/")
def root():

    return {
        "message": "HRMS API is running"
    }
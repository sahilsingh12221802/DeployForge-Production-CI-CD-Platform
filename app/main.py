from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI(
    title="DeployForge",
    description="Employee Operations Management API",
    version="1.0.0",
)
Instrumentator().instrument(app).expose(app)

class Employee(BaseModel):
    name: str
    email: str
    department: str
    role: str


class EmployeeResponse(Employee):
    id: int


employees = [
    EmployeeResponse(
        id=1,
        name="John Doe",
        email="john.doe@deployforge.com",
        department="Engineering",
        role="DevOps Engineer",
    ),
    EmployeeResponse(
        id=2,
        name="Jane Smith",
        email="jane.smith@deployforge.com",
        department="Data",
        role="Data Analyst",
    ),
]


@app.get("/")
def root():
    return {
        "application": "DeployForge",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee.id == employee_id:
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found",
    )


@app.post("/employees")
def create_employee(employee: Employee):
    new_id = max([employee.id for employee in employees], default=0) + 1

    new_employee = EmployeeResponse(
        id=new_id,
        **employee.model_dump(),
    )

    employees.append(new_employee)

    return new_employee


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    for index, existing_employee in enumerate(employees):
        if existing_employee.id == employee_id:

            updated_employee = EmployeeResponse(
                id=employee_id,
                **employee.model_dump(),
            )

            employees[index] = updated_employee

            return updated_employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found",
    )


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, employee in enumerate(employees):
        if employee.id == employee_id:
            deleted_employee = employees.pop(index)

            return {
                "message": "Employee deleted successfully",
                "employee": deleted_employee,
            }

    raise HTTPException(
        status_code=404,
        detail="Employee not found",
    )
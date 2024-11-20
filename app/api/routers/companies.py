from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas.users import Company
import os

router = APIRouter(tags=["Companies endpoints"])

db = Database('localhost', 'root', os.environ['MARIADB_ROOT_PWD'], 'task_management')
conn = db.connect()
cur = db.get_cursor()


@router.get("/companies/")
def read_companies():
    cur.execute("SELECT * FROM Companies")
    companies = cur.fetchall()
    return [{"id": company[0], "company_name": company[1]} for company in companies]


@router.get("/companies/{company_id}")
def read_company(company_id: int):
    cur.execute("SELECT * FROM Companies WHERE id = ?", (company_id,))
    company = cur.fetchone()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"id": company[0], "company_name": company[1]}


@router.post("/companies/")
def create_company(company: Company):
    cur.execute("INSERT INTO Companies (company_name) VALUES (?)",
                (company.company_name,))
    conn.commit()
    return {"id": cur.lastrowid, "company_name": company.company_name}


@router.put("/companies/{company_id}")
def update_company(company_id: int, company: Company):
    cur.execute("UPDATE Companies SET company_name = ? WHERE id = ?",
                (company.company_name, company_id))
    conn.commit()
    return {"id": company_id, "company_name": company.company_name}


@router.delete("/companies/{company_id}")
def delete_company(company_id: int):
    cur.execute("DELETE FROM Companies WHERE id = ?", (company_id,))
    conn.commit()
    return {"message": "Company deleted"}

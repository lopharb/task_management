from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.model.base import Base
from app.model.user import Company
from app.schemas.company import CompanyResponse, CompanyCreate
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.model.base import Base

router = APIRouter(tags=["Companies"], prefix="/api")


PASSWORD = os.environ.get("MARIADB_ROOT_PWD")
DATABASE_URL = f'mariadb+mariadbconnector://root:{PASSWORD}@localhost:3306/TM_alchemy'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/companies/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/companies/", response_model=List[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies


@router.get("/companies/{company_id}", response_model=CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.delete("/companies/{company_id}", response_model=dict)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

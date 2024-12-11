from pydantic import BaseModel


class CompanyCreate(BaseModel):
    company_name: str


class CompanyResponse(CompanyCreate):
    id: int

    class Config:
        orm_mode = True

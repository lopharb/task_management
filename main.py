from fastapi import FastAPI
from app.api.routers import task_routers, user_routers, role_routers, company_routers, worklog_routers

app = FastAPI()

app.include_router(task_routers.router)
app.include_router(user_routers.router)
app.include_router(role_routers.router)
app.include_router(company_routers.router)
app.include_router(worklog_routers.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
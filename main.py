import uvicorn
from fastapi import FastAPI
from app.api.routers import users, companies, roles, tasks, worklogs

app = FastAPI()

app.include_router(users.router)
app.include_router(companies.router)
app.include_router(roles.router)
app.include_router(tasks.router)
app.include_router(worklogs.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

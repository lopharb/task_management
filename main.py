from fastapi import FastAPI
from app.api.routers import task_routers, user_routers, role_routers, company_routers, worklog_routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(task_routers.router)
app.include_router(user_routers.router)
app.include_router(role_routers.router)
app.include_router(company_routers.router)
app.include_router(worklog_routers.router)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

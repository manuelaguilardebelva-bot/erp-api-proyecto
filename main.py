from fastapi import FastAPI
from timesheets_router import router as timesheets_router

app = FastAPI(title="ERP API")

app.include_router(timesheets_router)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al ERP"}

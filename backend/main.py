import os
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from backend.fleet.models import Base
from backend.db import engine
from backend.fleet.router import router as fleet_router
from backend.monitoring.metrics import router as metrics_router
from backend.admin.router import router as admin_router
from backend.payments.router import router as payments_router
import yaml

app = FastAPI(title="Crubotics Agro — Core Production")

if not os.path.exists("static"): os.makedirs("static", exist_ok=True)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.include_router(fleet_router)
app.include_router(metrics_router)
app.include_router(admin_router)
app.include_router(payments_router)

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/openapi.yaml")
def openapi_yaml():
    return Response(yaml.dump(app.openapi()), media_type="application/yaml")

if os.getenv("DATABASE_URL","").startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

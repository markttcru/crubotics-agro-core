from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
import json

from backend.db import SessionLocal
from .models import Robot, Task, Telemetry
from .schemas import RobotIn, RobotOut, TaskIn, TaskAssign, TaskOut, TelemetryIn
from backend.auth.jwt_roles import require_roles, get_claims

router = APIRouter(prefix="/api/fleet", tags=["fleet"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/robots", response_model=list[RobotOut])
def list_robots(db: Session = Depends(get_db), claims=Depends(get_claims)):
    roles = set(claims.get("roles", []))
    farms = claims.get("farms", [])
    stmt = select(Robot)
    if farms and not roles.intersection({"admin","manager","technician"}):
        stmt = stmt.where(Robot.farm_id.in_(farms))
    return db.execute(stmt).scalars().all()

@router.post("/robots", response_model=RobotOut, dependencies=[Depends(require_roles(["admin","manager","technician"]))])
def register_robot(payload: RobotIn, db: Session = Depends(get_db)):
    existing = db.execute(select(Robot).where(Robot.robot_uid == payload.robot_uid)).scalar_one_or_none()
    if existing: raise HTTPException(400, "Robot already registered")
    robot = Robot(robot_uid=payload.robot_uid, name=payload.name or "Robot", farm_id=payload.farm_id, farmer_name=payload.farmer_name, notes=payload.notes or "")
    db.add(robot); db.commit(); db.refresh(robot); return robot

@router.get("/robots/{robot_uid}", response_model=RobotOut)
def get_robot(robot_uid: str, db: Session = Depends(get_db), claims=Depends(get_claims)):
    robot = db.execute(select(Robot).where(Robot.robot_uid == robot_uid)).scalar_one_or_none()
    if not robot: raise HTTPException(404, "Robot not found")
    farms = claims.get("farms", [])
    roles = set(claims.get("roles", []))
    if farms and not roles.intersection({"admin","manager","technician"}) and robot.farm_id not in farms:
        raise HTTPException(403, "Forbidden")
    return robot

@router.post("/robots/{robot_uid}/telemetry", response_model=dict, dependencies=[Depends(require_roles(["admin","manager","technician","farmer"]))])
def push_telemetry(robot_uid: str, payload: TelemetryIn, db: Session = Depends(get_db)):
    robot = db.execute(select(Robot).where(Robot.robot_uid == robot_uid)).scalar_one_or_none()
    if not robot: raise HTTPException(404, "Robot not found")
    if payload.battery_pct is not None: robot.battery_pct = payload.battery_pct
    robot.last_seen = datetime.utcnow()
    tel = Telemetry(
        robot_id=robot.id, battery_pct=payload.battery_pct, lat=payload.lat, lon=payload.lon,
        soil_moisture=payload.soil_moisture, temperature_c=payload.temperature_c,
        task_status=payload.task_status, extra=json.dumps(payload.extra or {})
    )
    db.add(tel); db.commit(); return {"ok": True}

@router.get("/tasks", response_model=list[TaskOut])
def list_tasks(status: str | None = None, db: Session = Depends(get_db), claims=Depends(get_claims)):
    stmt = select(Task)
    farms = claims.get("farms", [])
    roles = set(claims.get("roles", []))
    if farms and not roles.intersection({"admin","manager","technician"}):
        stmt = stmt.where(Task.farm_id.in_(farms))
    if status: stmt = stmt.where(Task.status == status)
    return db.execute(stmt).scalars().all()

@router.post("/tasks", response_model=TaskOut, dependencies=[Depends(require_roles(["admin","manager","technician"]))])
def create_task(payload: TaskIn, db: Session = Depends(get_db)):
    t = Task(kind=payload.kind, crop=payload.crop, acres=payload.acres or 0.0, farm_id=payload.farm_id,
             priority=payload.priority or 5, status="queued", scheduled_for=payload.scheduled_for,
             payload=json.dumps(payload.payload or {}), created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(t); db.commit(); db.refresh(t); return t

@router.post("/tasks/{task_id}/assign", response_model=TaskOut, dependencies=[Depends(require_roles(["admin","manager","technician"]))])
def assign_task(task_id: int, assign: TaskAssign, db: Session = Depends(get_db)):
    t = db.get(Task, task_id); 
    if not t: raise HTTPException(404, "Task not found")
    robot = db.execute(select(Robot).where(Robot.robot_uid == assign.robot_uid)).scalar_one_or_none()
    if not robot: raise HTTPException(404, "Robot not found")
    t.robot_id = robot.id; t.status="assigned"; t.updated_at=datetime.utcnow(); db.commit(); db.refresh(t); return t

@router.post("/tasks/{task_id}/start", response_model=TaskOut, dependencies=[Depends(require_roles(["admin","manager","technician"]))])
def start_task(task_id: int, db: Session = Depends(get_db)):
    t = db.get(Task, task_id); 
    if not t: raise HTTPException(404, "Task not found")
    t.status="in_progress"; t.started_at=datetime.utcnow(); t.updated_at=datetime.utcnow(); db.commit(); db.refresh(t); return t

@router.post("/tasks/{task_id}/complete", response_model=TaskOut, dependencies=[Depends(require_roles(["admin","manager","technician"]))])
def complete_task(task_id: int, db: Session = Depends(get_db)):
    t = db.get(Task, task_id); 
    if not t: raise HTTPException(404, "Task not found")
    t.status="done"; t.completed_at=datetime.utcnow(); t.updated_at=datetime.utcnow(); db.commit(); db.refresh(t); return t

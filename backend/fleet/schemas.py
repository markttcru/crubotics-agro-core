from datetime import datetime
from pydantic import BaseModel

class RobotIn(BaseModel):
    robot_uid: str
    name: str | None = None
    farm_id: int | None = None
    farmer_name: str | None = None
    notes: str | None = None

class RobotOut(BaseModel):
    id: int; robot_uid: str; name: str | None; status: str
    farm_id: int | None = None; farmer_name: str | None = None
    battery_pct: float | None = None; last_seen: datetime | None = None
    notes: str | None = None
    class Config: from_attributes = True

class TelemetryIn(BaseModel):
    robot_uid: str
    battery_pct: float | None = None
    lat: float | None = None; lon: float | None = None
    soil_moisture: float | None = None; temperature_c: float | None = None
    task_status: str | None = None
    extra: dict | None = None

class TaskIn(BaseModel):
    kind: str
    crop: str | None = None
    acres: float | None = 0.0
    farm_id: int | None = None
    priority: int | None = 5
    scheduled_for: datetime | None = None
    payload: dict | None = None

class TaskAssign(BaseModel): robot_uid: str

class TaskOut(BaseModel):
    id:int; kind:str; crop:str|None=None; acres:float|None=0.0; farm_id:int|None=None
    priority:int; status:str; scheduled_for:datetime|None=None
    started_at:datetime|None=None; completed_at:datetime|None=None
    robot_id:int|None=None; payload:dict|None=None
    class Config: from_attributes = True

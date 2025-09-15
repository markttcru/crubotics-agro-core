from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    robot_uid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(128), default="Robot")
    status: Mapped[str] = mapped_column(String(32), default="idle")
    farm_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    farmer_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    battery_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    telemetry = relationship("Telemetry", back_populates="robot", cascade="all,delete")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    crop: Mapped[str | None] = mapped_column(String(64), nullable=True)
    acres: Mapped[float] = mapped_column(Float, default=0.0)
    farm_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    scheduled_for: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    robot_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("robots.id"), nullable=True)
    payload: Mapped[str] = mapped_column(Text, default="{}")

class Telemetry(Base):
    __tablename__ = "telemetry"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    robot_id: Mapped[int] = mapped_column(Integer, ForeignKey("robots.id", ondelete="CASCADE"), nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    battery_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    soil_moisture: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    task_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    extra: Mapped[str] = mapped_column(Text, default="{}")
    robot = relationship("Robot", back_populates="telemetry")

# Crubotics Agro — Core Production (Single Division)

This is a clean rollback to the **Agro-only** platform with:
- RBAC JWT (admin/manager/technician/farmer) with farm scoping
- Robots / Tasks / Telemetry models (no orgs/divisions)
- Admin token mint endpoint
- Payments stubs (WiPay, Blink) — division-agnostic
- Alembic migrations (Postgres), Dockerfile, Railway config

## Deploy
1) Set `DATABASE_URL` to Postgres and `JWT_SECRET`.
2) Run migrations: `alembic upgrade head`
3) Start: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

Build: 20250913_214230

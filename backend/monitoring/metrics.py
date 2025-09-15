from fastapi import APIRouter
from prometheus_client import CollectorRegistry, Counter, generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()

_registry = CollectorRegistry()
requests_total = Counter("requests_total", "Total requests", registry=_registry)

@router.get("/metrics")
def metrics():
    return generate_latest(_registry)

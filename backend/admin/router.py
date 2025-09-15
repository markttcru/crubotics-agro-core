from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List
from backend.auth.jwt_roles import create_token, require_roles

router = APIRouter(prefix="/api/admin", tags=["admin"])

class MintIn(BaseModel):
    sub: str = Field(..., description="User identifier")
    roles: List[str] = Field(default_factory=list)
    farms: List[int] = Field(default_factory=list)
    exp_seconds: int = Field(default=3600)

@router.post("/mint-token", dependencies=[Depends(require_roles(["admin"]))])
def mint_token(payload: MintIn):
    token = create_token(sub=payload.sub, roles=payload.roles, farms=payload.farms, exp_seconds=payload.exp_seconds)
    return {"token": token}

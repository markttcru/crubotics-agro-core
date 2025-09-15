import os, time
from typing import List, Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "crubotics-api")
JWT_ISSUER  = os.getenv("JWT_ISSUER",  "crubotics")

security = HTTPBearer(auto_error=True)

def create_token(sub: str, roles: List[str], farms: Optional[list[int]] = None, exp_seconds: int = 3600) -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "roles": roles,
        "farms": farms or [],
        "aud": JWT_AUDIENCE,
        "iss": JWT_ISSUER,
        "iat": now,
        "exp": now + exp_seconds,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

def require_roles(allowed: List[str]):
    def dep(payload = Depends(verify_token)):
        user_roles = set(payload.get("roles", []))
        if not user_roles.intersection(allowed):
            raise HTTPException(status_code=403, detail="Forbidden")
        return payload
    return dep

def get_claims(payload = Depends(verify_token)):
    return payload

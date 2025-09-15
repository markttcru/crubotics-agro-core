from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/payments", tags=["payments"])

class InitPaymentIn(BaseModel):
    amount: float
    currency: str = "TTD"
    reference: str

@router.post("/wipay/initiate")
def wipay_initiate(payload: InitPaymentIn):
    return {
        "provider": "wipay",
        "status": "created",
        "pay_url": f"https://sandbox.wipayfinancial.com/pay?ref={payload.reference}&amount={payload.amount}&currency={payload.currency}",
        "echo": payload.dict(),
    }

@router.post("/blink/initiate")
def blink_initiate(payload: InitPaymentIn):
    return {
        "provider": "blink",
        "status": "created",
        "deep_link": f"blink://pay?ref={payload.reference}&amount={payload.amount}&currency={payload.currency}",
        "echo": payload.dict(),
    }

@router.post("/wipay/webhook")
async def wipay_webhook(req: Request):
    data = await req.json()
    return {"ok": True, "received": data}

@router.post("/blink/webhook")
async def blink_webhook(req: Request):
    data = await req.json()
    return {"ok": True, "received": data}

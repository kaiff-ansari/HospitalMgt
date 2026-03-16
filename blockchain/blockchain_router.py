from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from blockchain.blockservice import verify_chain,fix_tampered_block
from auth.ouath2 import get_admin

router = APIRouter(prefix="/blockchain")

@router.get("/verify")
def verify_blockchain(db: Session = Depends(get_db), current_admin = Depends(get_admin)):
    
    result = verify_chain(db)
    
    if result["valid"]:
        return {
            "message": "Blockchain is valid",
            "total_blocks": result["total_blocks"]
        }
    
    return {
        "message": "Blockchain tampered",
        "tampered_at_block": result["tampered_at_block"],
        "reason": result["reason"]
    }
    
    
@router.post("/fix/{block_id}")
def fix_block(block_id: int, db: Session = Depends(get_db),current_admin = Depends(get_admin)):
    result = fix_tampered_block(db, block_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["reason"])
    return result    
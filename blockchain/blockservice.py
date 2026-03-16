import json
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.blockchain_model import BlockChainAudit
from blockchain.hashservice import generate_hash
from fastapi import HTTPException


def add_block(db: Session, record_id: int, table_name: str, data: dict):

    
    last_block = (
        db.execute(
            select(BlockChainAudit)
            .order_by(BlockChainAudit.id.desc())
            .limit(1)
            .with_for_update()
        ).scalars().first()
    )

    if last_block:
     previous_hash = last_block.current_hash
     
    else:
     previous_hash = "0"

    # Previous hash bhi data mein include — stronger linking
    block_data = {
        **data,
        "previous_hash": previous_hash,
        "table_name": table_name,
        "record_id": record_id,
    }

    current_hash = generate_hash(block_data)

    new_block = BlockChainAudit(
        record_id=record_id,
        table_name=table_name,
        previous_hash=previous_hash,
        current_hash=current_hash,
        data=json.dumps(data)  # audit trail ke liye original data store
    )

    db.add(new_block)
    db.commit()
    db.refresh(new_block)
    return new_block

def verify_chain(db: Session) -> dict:

    blocks = (
        db.query(BlockChainAudit)
        .order_by(BlockChainAudit.id.asc())
        .all()
    )

    if not blocks:
        return {"valid": True, "total_blocks": 0}

    # Genesis block bhi check karo
    for i in range(len(blocks)):
        current_block = blocks[i]

        if current_block.data:
            stored_data = json.loads(current_block.data)
            block_data = {
                **stored_data,
                "previous_hash": current_block.previous_hash,
                "table_name": current_block.table_name,
                "record_id": current_block.record_id,
            }
            recomputed_hash = generate_hash(block_data)

            if recomputed_hash != current_block.current_hash:
                return {
                    "valid": False,
                    "tampered_at_block": current_block.id,
                    "reason": "Hash mismatch — data tampered in DB"
                }

    
        if i > 0:
            previous_block = blocks[i - 1]
            if current_block.previous_hash != previous_block.current_hash:
                return {
                    "valid": False,
                    "tampered_at_block": current_block.id,
                    "reason": "Chain link broken — previous_hash mismatch"
                }

    return {"valid": True, "total_blocks": len(blocks)}


def fix_tampered_block(db: Session, block_id: int) -> dict:

    block = db.query(BlockChainAudit).filter(BlockChainAudit.id == block_id).first()

    if not block:
        return {"success": False, "reason": "Block not found"}

    if not block.data:
        return {"success": False, "reason": "Original data missing — cannot fix"}

    # recomputer hash from data
    stored_data = json.loads(block.data)
    block_data = {
        **stored_data,
        "previous_hash": block.previous_hash,
        "table_name": block.table_name,
        "record_id": block.record_id,
    }

    correct_hash = generate_hash(block_data)

    # storing current hash
    block.current_hash = correct_hash
    db.commit()

    return {
        "success": True,
        "fixed_block": block_id,
        "restored_hash": correct_hash
    }
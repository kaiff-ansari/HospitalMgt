from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.blood_schema import BloodInventoryCreate
from models.blood_inventory import BloodInventory
from blockchain.blockservice import add_block,verify_chain



def add_inventory(db:Session, blood:BloodInventoryCreate):
    
    inventory = BloodInventory(
         blood_group = blood.blood_group,
        rh_factor = blood.rh_factor,
        expire_date = blood.expire_date,
        status = blood.status,
        notes = blood.notes
        
    )
    
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    
    data = {
         "id" : inventory.id,
         "blood_group" : inventory.blood_group,
         "rh_factor" : inventory.rh_factor,
         "expire_date" : str (inventory.expire_date),
         "status" : inventory.status,
         "notes" : inventory.notes
         
    }
    
    add_block(db,inventory.id,"blood_inventory", data)
    return inventory


def get_all_inventory(db: Session):

    inventory = db.query(BloodInventory).all()

    if not inventory:
        raise HTTPException(status_code=404, detail="No blood inventory found")

    return inventory    


def update_inventory(db:Session, inventory_id:int, inventory_data:BloodInventoryCreate):
    
    chain_status = verify_chain(db)   
    
    if not chain_status["valid"]:
        raise HTTPException(
             status_code=409,
            detail=f"Blockchain integrity compromised: {chain_status['reason']}"
        ) 
        
        
    inventory = db.query(BloodInventory).filter(BloodInventory.id == inventory_id).first()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found ")
    
    
    inventory.blood_group = inventory_data.blood_group,
    inventory.rh_factor = inventory_data.rh_factor,
    inventory.expire_date = inventory_data.expire_date,
    inventory.status = inventory_data.status
    inventory.notes = inventory_data.notes
    
    db.commit()
    db.refresh(inventory)
    
    data = {
        "id" : inventory.id,
         "blood_group" : inventory.blood_group,
         "rh_factor" : inventory.rh_factor,
         "expire_date" : str (inventory.expire_date),
         "status" : inventory.status,
         "notes" : inventory.notes
    }
    
    add_block(db,inventory.id, "blood_inventory",data)
    return inventory
 
 
def delete_blood_inventory(db: Session, inventory_id: int):

    
    chain_status = verify_chain(db)
    if not chain_status["valid"]:
        raise HTTPException(
            status_code=409,
            detail=f"Blockchain integrity compromised: {chain_status['reason']}"
        )

    inventory = db.query(BloodInventory).filter(BloodInventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    data = {
        "id": inventory.id,
        "blood_group": inventory.blood_group,
        "rh_factor": inventory.rh_factor,
        "expire_date": str(inventory.expire_date),
        "status": inventory.status,
        "notes": inventory.notes,
        "action": "deleted"
    }

    
    add_block(db, inventory.id, "blood_inventory", data)

    db.delete(inventory)
    db.commit()

    return {"message": "Blood inventory deleted successfully"}        
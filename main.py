from fastapi import FastAPI
from models import doctor_model
from database.connection import engine
from routers import doctors_router, auth_router,inventory_router
from models import blockchain_model
from blockchain.blockchain_router import router as blockchain_router


app = FastAPI()


doctor_model.Base.metadata.create_all(bind=engine)
blockchain_model.Base.metadata.create_all(bind=engine)

app.include_router(doctors_router.router)
app.include_router(auth_router.router)
app.include_router(blockchain_router)
app.include_router(inventory_router.router)



@app.get("/")
def HealtCheck():
    return "Hii"
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from routers import auth, flowers, orders, flowersinorder

load_dotenv(".env")
app = FastAPI(title="DataGO Flowers Service", version="0.0.1")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(auth.ROUTER)
app.include_router(flowers.ROUTER)
app.include_router(orders.ROUTER)
app.include_router(flowersinorder.ROUTER)

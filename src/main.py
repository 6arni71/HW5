from fastapi import FastAPI
from api import get_all, get_known, get_new, get_query, info
from es_connector import init_db

app = FastAPI()

app.include_router(init_db.router)
app.include_router(info.router)
app.include_router(get_all.router)
app.include_router(get_known.router)
app.include_router(get_new.router)
app.include_router(get_query.router)



from fastapi import FastAPI
from app.api.api import api_router
from app.core.cors import configure_cors

app = FastAPI(title="JHECAS Backend")
configure_cors(app)
app.include_router(api_router)

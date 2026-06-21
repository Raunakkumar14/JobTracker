
from fastapi import FastAPI
from app.routes import auth
from app.routes import job
from app.routes import user
app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(job.router)


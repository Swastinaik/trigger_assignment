from fastapi import FastAPI
from app.routers import attendance, subscriptions, members, plans
from app.seed import seed_data
from sqlmodel import SQLModel
from app.database import engine, run_sql_file, AsyncSessionLocal
from pathlib import Path
from sqlalchemy import text

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # create tables from SQLModel models
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    # apply the trigger (ensure path is correct)
    await run_sql_file(Path(__file__).parent.joinpath("sql/triggers.sql"))

    # seed data
    async with AsyncSessionLocal() as session:
        await seed_data(session)


app.include_router(attendance.router)
app.include_router(subscriptions.router)
app.include_router(members.router)
app.include_router(plans.router)



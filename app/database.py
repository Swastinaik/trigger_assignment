# app/database.py
import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pathlib import Path

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/service_membership"
)


print(f"DEBUG: DATABASE_URL={DATABASE_URL}")
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# helper to run raw SQL files (eg triggers.sql) at startup
# helper to run raw SQL files (eg triggers.sql) at startup
def split_sql_statements(sql: str):
    statements = []
    buffer = []
    in_dollar_quote = False
    i = 0
    while i < len(sql):
        char = sql[i]
        # Check for $$ marker
        if char == '$' and i + 1 < len(sql) and sql[i+1] == '$':
            in_dollar_quote = not in_dollar_quote
            buffer.append(char)
            buffer.append(sql[i+1])
            i += 2
            continue
        
        if char == ';' and not in_dollar_quote:
            stmt = "".join(buffer).strip()
            if stmt:
                statements.append(stmt)
            buffer = []
        else:
            buffer.append(char)
        i += 1
    
    # Add any remaining statement
    if buffer:
        stmt = "".join(buffer).strip()
        if stmt:
            statements.append(stmt)
    return statements

async def run_sql_file(path: str):
    sql_content = Path(path).read_text()
    statements = split_sql_statements(sql_content)
    
    async with engine.begin() as conn:
        for statement in statements:
            # text() required for SQLAlchemy
            await conn.execute(text(statement))


def create_db_and_triggers():
    SQLModel.metadata.create_all(engine)
    trigger_sql = text("""
    CREATE OR REPLACE FUNCTION fn_inc_member_checkins()
    RETURNS TRIGGER AS $$
    BEGIN
      UPDATE "member" SET total_check_ins = total_check_ins + 1 WHERE id = NEW.member_id;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    DROP TRIGGER IF EXISTS trg_attendance_after_insert ON attendance;
    
    CREATE TRIGGER trg_attendance_after_insert
    AFTER INSERT ON attendance
    FOR EACH ROW
    EXECUTE FUNCTION fn_inc_member_checkins();
    """)
    

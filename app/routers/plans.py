from fastapi import APIRouter, Form, Depends
from typing import Annotated
from app.models import Plan
from datetime import datetime
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post('/')
async def create_plan(name: Annotated[str, Form()], duration_days: Annotated[int, Form()], price: Annotated[float, Form()], session: AsyncSession = Depends(get_session)):
    if(name is None or duration_days is None or price is None):
        raise ValueError("Name, duration_days, and price are required")
    
    plan = Plan(name=name, duration_days=duration_days, price=price, created_at=datetime.now())
    session.add(plan)
    await session.commit()
    await session.refresh(plan)
    return plan


@router.get('/')
async def get_plans(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Plan))
    plans = result.scalars().all()
    return plans

@router.delete('/')
async def delete_plan(id: Annotated[int, Form()], session: AsyncSession = Depends(get_session)):
    plan = await session.get(Plan, id)
    if plan is None:
        raise ValueError("Plan not found")
    await session.delete(plan)
    await session.commit()
    return {"message": "Plan deleted successfully"}

from fastapi import APIRouter, Form, Depends, HTTPException
from datetime import date
from typing import Annotated
from app.models import Plan, Member, Subscription, Attendance
from datetime import datetime
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

router = APIRouter(prefix='/attendance', tags=['attendance'])

@router.post('/check-in')
async def check_in(member_id: Annotated[int, Form(...)], session: AsyncSession = Depends(get_session)):
    if not member_id:
        raise HTTPException(status_code=400, detail='Bad Request')
    statement = select(Subscription).where(Subscription.member_id == member_id)
    result = await session.execute(statement)
    subscription = result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail='No active subscription for this member.')
    attendance = Attendance(member_id=member_id, date=date.today(), check_in_time=datetime.now())

    session.add(attendance)
    await session.commit()
    return {'message': 'Check-in successful'}



@router.get('/members/{member_id}/attendance')
async def get_attendance(member_id: int, session: AsyncSession = Depends(get_session)):
    if not member_id:
        raise HTTPException(status_code=400, detail='Bad Request')
    member = await session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail='Member not found')
    return member.total_check_ins

   

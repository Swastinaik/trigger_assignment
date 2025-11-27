from fastapi import APIRouter, Form, Depends
from typing import Annotated
from sqlmodel import select
from app.models import Member
from datetime import datetime
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/members", tags=["members"])


@router.post('/')
async def create_member(phone: Annotated[str, Form()], name: Annotated[str, Form()], session: AsyncSession = Depends(get_session)):
    if(phone is None or name is None):
        raise HTTPException(status_code=400, detail='Bad Request')
    member = Member(name=name, phone=phone, join_date=datetime.now())
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member


@router.get('/')
async def get_members(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Member))
    members = result.scalars().all()
    return members



    

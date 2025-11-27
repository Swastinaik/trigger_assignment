from fastapi import APIRouter, Form, Depends, HTTPException
from datetime import date
from typing import Annotated
from app.models import Plan,Member, Subscription
from datetime import datetime, timedelta
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import BaseModel

router = APIRouter(prefix='/subscription', tags=['subscriptions'])

class SubscriptionCreateRequest(BaseModel):
    member_id: int
    plan_id: int
    start_date: date

@router.post('/')
async def create_subscriptions_users(member_id: Annotated[int, Form(...)], plan_id: Annotated[int, Form(...)],start_date: Annotated[date, Form(...)], session: AsyncSession = Depends(get_session)):
    """
    subscription_data: SubscriptionCreateRequest
     member_id = subscription_data.member_id
    plan_id = subscription_data.plan_id
    start_date = subscription_data.start_date
    """ 
    if not member_id or not plan_id:
        raise HTTPException(status_code=400, detail='Bad Request')
    member = await session.get(Member, member_id)
    plan = await session.get(Plan, plan_id)
    print(plan)
    if not plan:
        raise HTTPException(status_code=404, detail='Plan not found')
    subscription = Subscription(member_id=member_id, plan_id=plan_id, start_date=start_date, end_date=start_date + timedelta(days=plan.duration_days))
    session.add(subscription)
    await session.commit()
    return {'message': 'Subscription created successfully'}


@router.get('/')
async def get_subscriptions(session: AsyncSession = Depends(get_session)):
    subscriptions = await session.exec(select(Subscription))
    return subscriptions.all()

@router.delete('/')
async def delete_subscription(subscription_id: Annotated[int, Form(...)], session: AsyncSession = Depends(get_session)):
    subscription = await session.get(Subscription, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    await session.delete(subscription)
    await session.commit()
    return {'message': 'Subscription deleted successfully'}


@router.get('/members/{member_id}/current-subscription')
async def get_current_subscription(member_id: int, session: AsyncSession = Depends(get_session)):
    today = date.today()
    subscription = await session.exec(select(Subscription).where(Subscription.member_id == member_id))
    subscription = subscription.one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    if subscription.start_date > today or subscription.end_date < today:
        raise HTTPException(status_code=404, detail='Subscription not found')
    return subscription

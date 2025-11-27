# app/seed.py
from sqlmodel import select
from datetime import date, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Member, Plan, Subscription, Status, PlanType


async def seed_data(session: AsyncSession):
    # Check if already seeded (avoid duplicate inserts)
    result = await session.execute(select(Plan))
    existing_plan = result.scalars().first()
    if existing_plan:
        print("🌱 Seed data already exists. Skipping seeding...")
        return

    print("🌱 Seeding database with default data...")

    # ---------- Create Plans ----------
    monthly = Plan(name=PlanType.Monthly, price=800, duration_days=30)
    quarterly = Plan(name=PlanType.Quarterly, price=2100, duration_days=90)
    yearly = Plan(name=PlanType.Yearly, price=7500, duration_days=365)

    session.add_all([monthly, quarterly, yearly])
    await session.commit()
    await session.refresh(monthly)
    await session.refresh(quarterly)
    await session.refresh(yearly)

    # ---------- Create Members ----------
    member1 = Member(
        name="Alice Johnson",
        phone="9876543210",
        join_date=date.today() - timedelta(days=10),
        status=Status.active,
    )

    member2 = Member(
        name="Bob Smith",
        phone="9123456780",
        join_date=date.today() - timedelta(days=25),
        status=Status.active,
    )

    session.add_all([member1, member2])
    await session.commit()
    await session.refresh(member1)
    await session.refresh(member2)

    # ---------- Create Active Subscriptions ----------
    sub1 = Subscription(
        member_id=member1.id,
        plan_id=monthly.id,
        start_date=date.today() - timedelta(days=5),
        end_date=date.today() + timedelta(days=25)
    )

    sub2 = Subscription(
        member_id=member2.id,
        plan_id=quarterly.id,
        start_date=date.today() - timedelta(days=20),
        end_date=date.today() + timedelta(days=70)
    )

    session.add_all([sub1, sub2])
    await session.commit()

    print("🌱 Data seeding completed successfully!")

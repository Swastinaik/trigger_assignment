from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime
from typing import  Literal
from enum import Enum
from datetime import datetime, date


class Status(Enum):
    active = 'active'
    inactive = 'inactive'

class PlanType(Enum):
    Monthly = 'Monthly'
    Quarterly = 'Quarterly'
    Yearly = 'Yearly'


class Member(SQLModel, table=True):
    id: int| None = Field(primary_key=True, default=None)
    name: str
    phone: str
    join_date: date
    status: Status = Field(default=Status.active)
    total_check_ins: int = Field(default=0, nullable=False)


class Plan(SQLModel, table= True):
    id: int| None = Field(primary_key=True, default=None)
    name: PlanType = Field(default=PlanType.Monthly)
    price: int
    duration_days: int 


class Subscription(SQLModel, table= True):
    id: int| None = Field(primary_key=True, default=None)
    member_id: int = Field(foreign_key="member.id")
    plan_id: int = Field(foreign_key="plan.id")
    start_date: date
    end_date: date


class Attendance(SQLModel, table= True):
    id: int| None = Field(primary_key=True, default=None)
    member_id: int = Field(foreign_key="member.id")
    date: date
    check_in_time: datetime
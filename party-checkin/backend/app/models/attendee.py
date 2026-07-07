from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from datetime import datetime
from app.database import Base


class Attendee(Base):

    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    signum = Column(String, unique=True, nullable=False)

    meal = Column(String)

    beverage = Column(String)

    checked_in = Column(Boolean, default=False)

    checkin_time = Column(DateTime)

    source = Column(String, default="RSVP")
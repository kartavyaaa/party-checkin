from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendee import Attendee

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):

    attendees = db.query(Attendee).all()

    total = len(attendees)

    checked_in = sum(1 for a in attendees if a.checked_in)

    pending = total - checked_in

    walkins = sum(1 for a in attendees if a.source == "Walk-In")

    people = []

    for attendee in attendees:

        people.append({

            "name": attendee.name,

            "signum": attendee.signum,

            "checked_in": attendee.checked_in,

            "time": attendee.checkin_time.strftime("%I:%M %p")
            if attendee.checkin_time else "",

            "source": attendee.source

        })

    return {

        "total": total,

        "checked_in": checked_in,

        "pending": pending,

        "walkins": walkins,

        "attendees": people

    }
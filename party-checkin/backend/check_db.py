from app.database import SessionLocal
from app.models.attendee import Attendee

db = SessionLocal()

for attendee in db.query(Attendee).all():
    print(attendee.signum, "|", attendee.name)
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.attendee import Attendee
from app.models.schemas import WalkInRegistration

router = APIRouter(prefix="/checkin", tags=["Check-In"])


@router.get("/{signum}")
def lookup(signum: str, db: Session = Depends(get_db)):

    attendee = (
        db.query(Attendee)
        .filter(
            func.lower(Attendee.signum) == signum.strip().lower()
        )
        .first()
    )

    if attendee is None:
        raise HTTPException(
            status_code=404,
            detail="Attendee not found"
        )

    return {
        "name": attendee.name,
        "signum": attendee.signum,
        "meal": attendee.meal,
        "beverage": attendee.beverage,
        "checked_in": attendee.checked_in,
        "checkin_time": attendee.checkin_time.strftime("%I:%M %p")
        if attendee.checkin_time else None,
    }

@router.post("/register")
def register_walkin(
    attendee: WalkInRegistration,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Attendee)
        .filter(
            func.lower(Attendee.signum) == attendee.signum.strip().lower()
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Signum already exists."
        )

    new_attendee = Attendee(
        name=attendee.name.strip(),
        signum=attendee.signum.strip().lower(),
        meal=attendee.meal,
        beverage=attendee.beverage,
        checked_in=True,
        checkin_time=datetime.now(),
        source="Walk-In",
    )

    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)

    return {
        "success": True,
        "message": "Walk-in registered successfully.",
        "name": new_attendee.name,
        "time": new_attendee.checkin_time.strftime("%I:%M %p"),
    }

@router.post("/{signum}")
def confirm(signum: str, db: Session = Depends(get_db)):

    attendee = (
        db.query(Attendee)
        .filter(
            func.lower(Attendee.signum) == signum.strip().lower()
        )
        .first()
    )

    if attendee is None:
        raise HTTPException(
            status_code=404,
            detail="Attendee not found"
        )

    if attendee.checked_in:
        return {
            "success": False,
            "message": "Already checked in",
            "time": attendee.checkin_time.strftime("%I:%M %p")
            if attendee.checkin_time else None,
        }

    attendee.checked_in = True
    attendee.checkin_time = datetime.now()

    db.commit()
    db.refresh(attendee)

    return {
        "success": True,
        "message": "Welcome!",
        "time": attendee.checkin_time.strftime("%I:%M %p"),
    }



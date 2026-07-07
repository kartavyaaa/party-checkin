from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.models.attendee import Attendee


class ImportService:

    def __init__(self, db: Session):
        self.db = db

    def import_excel(self, excel_path: str):

        excel_path = Path(excel_path)

        if not excel_path.exists():
            raise FileNotFoundError(excel_path)

        df = pd.read_excel(excel_path)

        # Normalize column names
        df.columns = [c.strip() for c in df.columns]

        # ---------- CHANGE THESE TO MATCH YOUR EXCEL ----------
        NAME_COLUMN = "Name"
        SIGNUM_COLUMN = "Signum"
        MEAL_COLUMN = "Meal Preference"
        BEVERAGE_COLUMN = "Beverage Preference"
        # -----------------------------------------------------

        imported = 0
        skipped = 0

        for _, row in df.iterrows():

            name = str(row[NAME_COLUMN]).strip()

            signum = str(row[SIGNUM_COLUMN]).strip().lower()

            meal = (
                str(row[MEAL_COLUMN]).strip()
                if pd.notna(row[MEAL_COLUMN])
                else ""
            )

            beverage = (
                str(row[BEVERAGE_COLUMN]).strip()
                if pd.notna(row[BEVERAGE_COLUMN])
                else ""
            )

            existing = (
                self.db.query(Attendee)
                .filter(Attendee.signum == signum)
                .first()
            )

            if existing:
                skipped += 1
                continue

            attendee = Attendee(
                name=name,
                signum=signum,
                meal=meal,
                beverage=beverage,
                source="RSVP",
            )

            self.db.add(attendee)
            imported += 1

        self.db.commit()

        return {
            "imported": imported,
            "skipped": skipped,
        }
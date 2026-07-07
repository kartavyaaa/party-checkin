from app.database import Base, engine, SessionLocal

# Import models so SQLAlchemy registers them
from app.models.attendee import Attendee

from app.services.import_service import ImportService

EXCEL_FILE = "responses.xlsx"

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


def main():
    db = SessionLocal()

    service = ImportService(db)

    result = service.import_excel(EXCEL_FILE)

    print("\n========== IMPORT COMPLETE ==========")
    print(result)
    print("=====================================")


if __name__ == "__main__":
    main()
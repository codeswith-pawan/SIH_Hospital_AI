"""
Create all database tables.
"""

from src.database.database import Base, engine

# Import models so SQLAlchemy registers all tables
from src.database import models  # noqa: F401


def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
    print("Tables created:")

    for table_name in Base.metadata.tables:
        print("-", table_name)


if __name__ == "__main__":
    init_database()

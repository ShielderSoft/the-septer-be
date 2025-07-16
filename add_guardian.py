from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from core.security import encrypt_password
# --------------------
# CONFIGURATION
# --------------------
DATABASE_URL = "sqlite:///septer.db"  # Or your actual DB path
GUARDIAN_EMAIL = "puja@rntinfosec.in"
GUARDIAN_PASSWORD = encrypt_password("Asdf2580@")

# --------------------
# SQLAlchemy Setup
# --------------------
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# --------------------
# Main Logic
# --------------------
def add_guardian():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    existing_user = session.query(User).filter_by(email=GUARDIAN_EMAIL).first()
    if existing_user:
        print(f"User {GUARDIAN_EMAIL} already exists.")
        return

    guardian = User(
        id="admin",
        email=GUARDIAN_EMAIL,
        role="Guardian",
        password=GUARDIAN_PASSWORD,
        created_at=datetime.utcnow()
    )
    session.add(guardian)
    session.commit()
    print(f"Guardian user '{GUARDIAN_EMAIL}' added successfully.")

if __name__ == "__main__":
    add_guardian()

from sqlmodel import SQLModel, Field, Session, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str | None = None
    is_active: bool = True

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
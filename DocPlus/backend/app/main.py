from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import engine, create_db_and_tables, get_session, User
from app.core.security import verify_password, get_password_hash, create_access_token

from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    
    with Session(engine) as session:
        admin_user = session.exec(select(User).where(User.email == "admin@docplus.com")).first()
        if not admin_user:
            new_admin = User(
                email="admin@docplus.com",
                hashed_password=get_password_hash("changethis"),
                full_name="Admin DocPlus",
                is_active=True
            )
            session.add(new_admin)
            session.commit()
            print("✅ Userul admin@docplus.com a fost creat cu succes!")
    yield 

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan, 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/login/access-token", tags=["login"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email sau parolă incorectă.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

if api_router:
    app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bine ai venit la DocPlus API!"}

@app.get("/health")
async def health():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
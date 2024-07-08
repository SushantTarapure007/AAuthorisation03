from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth, dependencies, database
from fastapi.security import OAuth2PasswordRequestForm
from .auth import Token

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.SessionLocal)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal), current_user: schemas.UserResponse = Depends(dependencies.admin_only)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(auth.get_current_active_user)):
    return current_user

@app.get("/admin/", response_model=schemas.UserResponse)
async def admin_route(current_user: schemas.UserResponse = Depends(dependencies.admin_only)):
    return current_user

@app.get("/manager/", response_model=schemas.UserResponse)
async def manager_route(current_user: schemas.UserResponse = Depends(dependencies.manager_only)):
    return current_user

@app.get("/user/", response_model=schemas.UserResponse)
async def user_route(current_user: schemas.UserResponse = Depends(dependencies.user_only)):
    return current_user

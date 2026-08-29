from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db
from security import hash_password, verify_password
from auth import create_access_token


templates = Jinja2Templates(directory="templates")


# =========================================================
# API ROUTER
# =========================================================

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


# =========================================================
# API REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=schemas.UserResponse
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================================
# API LOGIN
# =========================================================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# WEB ROUTER
# =========================================================

web_router = APIRouter()


# =========================================================
# WEB REGISTER
# =========================================================

@web_router.post("/register")
def register_web(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db)
):

    if len(password) < 8:

        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "error": "Password must be at least 8 characters long"
            },
            status_code=400
        )

    existing_user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if existing_user:

        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "error": "Username already exists"
            },
            status_code=400
        )

    hashed_password = hash_password(password)

    new_user = models.User(
        username=username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# =========================================================
# WEB LOGIN
# =========================================================

@web_router.post("/login")
def login_web(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if existing_user is None:

        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "error": "Invalid username or password"
            },
            status_code=401
        )

    password_valid = verify_password(
        password,
        existing_user.hashed_password
    )

    if not password_valid:

        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "error": "Invalid username or password"
            },
            status_code=401
        )

    access_token = create_access_token(
        existing_user.id
    )

    response = RedirectResponse(
        url="/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )

    return response
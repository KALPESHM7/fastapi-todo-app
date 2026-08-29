from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models

from database import get_db
from auth import get_current_user_from_cookie


router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user_from_cookie
    )
):

    tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    ).all()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "tasks": tasks,
            "username": current_user.username
        }
    )


@router.get("/login")
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "login.html"
    )


@router.get("/register")
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "register.html"
    )
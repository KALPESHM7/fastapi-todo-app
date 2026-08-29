# ==========================================
# USER ROUTES
# ==========================================

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models

from database import get_db

from auth import (
    get_current_user,
    get_current_user_from_cookie
)


# ==========================================
# TEMPLATES
# ==========================================

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    tags=["User"]
)


# ==========================================
# LOGOUT - POST
# ==========================================

@router.post("/logout")
def logout_post():

    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie(
        key="access_token"
    )

    return response


# ==========================================
# LOGOUT - GET
# ==========================================

@router.get("/logout")
def logout_get():

    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie(
        key="access_token"
    )

    return response


# ==========================================
# CURRENT USER
# ==========================================

@router.get("/me")
def get_me(
    current_user: models.User = Depends(
        get_current_user
    )
):

    return {
        "id": current_user.id,
        "username": current_user.username
    }


# ==========================================
# DASHBOARD
# ==========================================

@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user_from_cookie
    )
):

    # Get only the tasks belonging to
    # the currently logged-in user

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
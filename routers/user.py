# ==========================================
# USER ROUTES
# ==========================================

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

import models

from auth import (
    get_current_user,
    get_current_user_from_cookie
)


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
    current_user: models.User = Depends(
        get_current_user_from_cookie
    )
):

    return {
        "message": "Welcome to your dashboard",
        "user_id": current_user.id,
        "username": current_user.username
    }
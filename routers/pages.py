from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Pages"]
)


templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# LANDING PAGE
# ==========================================

@router.get("/")
def home(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "landing.html"
    )


# ==========================================
# LOGIN PAGE
# ==========================================

@router.get("/login")
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "login.html"
    )


# ==========================================
# REGISTER PAGE
# ==========================================

@router.get("/register")
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "register.html"
    )
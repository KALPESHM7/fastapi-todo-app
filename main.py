# ==========================================
# MAIN APPLICATION FILE
# ==========================================

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from auth import get_current_user, get_current_user_from_cookie

from routers import tasks, auth, pages, user

import models


# ==========================================
# DATABASE
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI()


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(tasks.router)

app.include_router(auth.router)

app.include_router(auth.web_router)

app.include_router(pages.router)

app.include_router(user.router)


# ==========================================
# GLOBAL ERROR HANDLER
# ==========================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )
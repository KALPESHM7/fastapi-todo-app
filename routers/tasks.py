# =========================================================
# TASK MANAGEMENT ROUTES
# =========================================================

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db
from auth import get_current_user_from_cookie


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =========================================================
# CREATE TASK
# =========================================================

@router.post("")
def create_task(
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):

    title = title.strip()

    if title == "":
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Task title cannot be empty"
            }
        )

    new_task = models.Task(
        title=title,
        owner_id=current_user.id,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "completed": new_task.completed
        }
    }


# =========================================================
# GET ALL TASKS
# =========================================================

@router.get("")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):

    tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    ).all()

    return tasks


# =========================================================
# GET SINGLE TASK
# =========================================================

@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =========================================================
# EDIT TASK
# =========================================================

@router.post("/{task_id}/edit")
def edit_task(
    task_id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    title = title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    task.title = title

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
    }


# =========================================================
# COMPLETE TASK
# =========================================================

@router.post("/{task_id}/complete")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = True

    db.commit()
    db.refresh(task)

    return {
        "message": "Task completed successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
    }


# =========================================================
# DELETE TASK
# =========================================================

@router.post("/{task_id}/delete")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }
from app.auth.deps import CurrentUser, get_current_user
from app.db.deps import get_db
from app.models.application import Application, ApplicationStatus
from app.models.status_event import StatusEvent
from app.schemas.application import (
    ApplicationCreate,
    ApplicationOut,
    ApplicationUpdate,
    StatusEventOut,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/applications", tags=["applications"])


def _get_owned_application_or_404(
    db: Session, application_id: int, user_id: int
) -> Application:
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == user_id)
        .first()
    )
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    status: ApplicationStatus | None = None,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    query = db.query(Application).filter(Application.user_id == current_user.id)
    if status is not None:
        query = query.filter(Application.status == status)
    return query.all()


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    data = payload.model_dump()
    data["user_id"] = current_user.id
    application = Application(**data)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return _get_owned_application_or_404(db, application_id, current_user.id)


@router.patch("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    application = _get_owned_application_or_404(db, application_id, current_user.id)
    updates = payload.model_dump(exclude_unset=True)

    if "status" in updates and updates["status"] != application.status:
        db.add(
            StatusEvent(
                application_id=application.id,
                from_status=application.status.value,
                to_status=updates["status"].value,
                source="manual",
            )
        )

    for field, value in updates.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    application = _get_owned_application_or_404(db, application_id, current_user.id)
    db.delete(application)
    db.commit()


@router.get("/{application_id}/status-events", response_model=list[StatusEventOut])
def list_status_events(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    _get_owned_application_or_404(db, application_id, current_user.id)
    return (
        db.query(StatusEvent)
        .filter(StatusEvent.application_id == application_id)
        .order_by(StatusEvent.id)
        .all()
    )

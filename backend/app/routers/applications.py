from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.application import Application, ApplicationStatus
from app.models.status_event import StatusEvent
from app.schemas.application import (
    ApplicationCreate,
    ApplicationOut,
    ApplicationUpdate,
    StatusEventOut,
)

router = APIRouter(prefix="/applications", tags=["applications"])


def _get_application_or_404(db: Session, application_id: int) -> Application:
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    user_id: int,
    status: ApplicationStatus | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Application).filter(Application.user_id == user_id)
    if status is not None:
        query = query.filter(Application.status == status)
    return query.all()


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    application = Application(**payload.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    return _get_application_or_404(db, application_id)


@router.patch("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)
):
    application = _get_application_or_404(db, application_id)
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
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = _get_application_or_404(db, application_id)
    db.delete(application)
    db.commit()


@router.get("/{application_id}/status-events", response_model=list[StatusEventOut])
def list_status_events(application_id: int, db: Session = Depends(get_db)):
    _get_application_or_404(db, application_id)
    return (
        db.query(StatusEvent)
        .filter(StatusEvent.application_id == application_id)
        .order_by(StatusEvent.id)
        .all()
    )

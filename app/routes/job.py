from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.job import Job
from app.schema.job import JobCreate, JobOut, JobUpdate

router = APIRouter(tags=["job"], prefix="/job")


@router.get("/", response_model=list[JobOut])
def get_jobs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    title: str | None = None,
    company: str | None = None,
    status: str | None = None,
    page:int=1,
    limit:int=5
):
    query = db.query(Job).filter(Job.user_id == current_user.id)

    if title:
        query = query.filter(Job.title.ilike(f"%{title}%"))
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if status:
        query = query.filter(Job.status == status)
    offset=(page-1)*limit

    return query.order_by(Job.id.desc()).offset(offset).limit(limit).all()


@router.get("/{job_id}", response_model=JobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == job_id,Job.user_id == current_user.id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/post", response_model=JobOut)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_job = Job(
        title=job.title,
        company=job.company,
        status=job.status,
        description=job.description,
        location=job.location,
        deadline=job.deadline,
        user_id=current_user.id,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id,
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in job_update.model_dump(exclude_unset=True).items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == job_id,
                                Job.user_id == current_user.id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job",
        )

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}

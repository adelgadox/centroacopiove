from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_coordinator, require_national_admin
from app.models.user import User
from app.schemas.campaign import CampaignCreate, CampaignOut, CampaignUpdate
from app.services.campaign_service import CampaignService
from app.utils.rate_limit import limiter

router = APIRouter(prefix="/v1/campaigns", tags=["campaigns"])


@router.get("", response_model=list[CampaignOut])
@limiter.limit("120/minute")
def list_campaigns(
    request: Request,
    active_only: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(require_coordinator),
):
    return CampaignService(db).list(active_only=active_only)


@router.get("/{campaign_id}", response_model=CampaignOut)
@limiter.limit("120/minute")
def get_campaign(
    request: Request,
    campaign_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_coordinator),
):
    return CampaignService(db).get(campaign_id)


@router.post("", response_model=CampaignOut, status_code=201)
@limiter.limit("20/hour")
def create_campaign(
    request: Request,
    data: CampaignCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_national_admin),
):
    return CampaignService(db).create(data)


@router.patch("/{campaign_id}", response_model=CampaignOut)
@limiter.limit("30/minute")
def update_campaign(
    request: Request,
    campaign_id: UUID,
    data: CampaignUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_national_admin),
):
    return CampaignService(db).update(campaign_id, data)

"""National dashboard and public needs endpoints."""

import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_center_role, tenant_scope
from app.models.user import User
from app.repositories.aggregate_repository import AggregateRepository
from app.schemas.aggregate import NationalDashboardOut, PublicNeedsOut
from app.utils import cache
from app.utils.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["dashboard"])

_DASHBOARD_TTL = 120   # 2 minutes — fresh enough, cheap enough
_PUBLIC_TTL = 300      # 5 minutes — cacheable at edge too


# ── Authenticated national dashboard ──────────────────────────────────────────

@router.get("/dashboard/national", response_model=NationalDashboardOut)
@limiter.limit("30/minute")
def national_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_center_role),
    scope: UUID | None = Depends(tenant_scope),
):
    """Aggregate dashboard.

    national_admin → all centers.
    coordinator/volunteer → their center only.
    """
    cache_key = f"dashboard:national:{str(scope) if scope else 'all'}"
    cached = cache.get(cache_key)
    if cached:
        return JSONResponse(content=json.loads(cached))

    repo = AggregateRepository(db)
    payload = NationalDashboardOut(
        totals=repo.summary_totals(center_id=scope),
        by_category=repo.stock_by_category(center_id=scope),
        by_center=repo.stock_by_center(center_id=scope),
        by_inn=repo.stock_by_inn(center_id=scope),
    )
    serialized = payload.model_dump_json()
    cache.set(cache_key, serialized, ttl=_DASHBOARD_TTL)
    return JSONResponse(content=json.loads(serialized))


# ── Public needs endpoint (no auth) ───────────────────────────────────────────

@router.get("/public/needs", response_model=PublicNeedsOut)
@limiter.limit("60/minute")
def public_needs(
    request: Request,
    db: Session = Depends(get_db),
):
    """Public read-only snapshot: what categories have sealed stock.

    No PII, no center names, no auth required.
    Cached in Redis; Cloudflare/Vercel CDN adds another cache layer via
    Cache-Control headers.
    """
    cache_key = "public:needs"
    cached = cache.get(cache_key)
    if cached:
        return JSONResponse(
            content=json.loads(cached),
            headers={"Cache-Control": f"public, max-age={_PUBLIC_TTL}, stale-while-revalidate=60"},
        )

    repo = AggregateRepository(db)
    payload = PublicNeedsOut(by_category=repo.needed_by_category())
    serialized = payload.model_dump_json()
    cache.set(cache_key, serialized, ttl=_PUBLIC_TTL)
    return JSONResponse(
        content=json.loads(serialized),
        headers={"Cache-Control": f"public, max-age={_PUBLIC_TTL}, stale-while-revalidate=60"},
    )

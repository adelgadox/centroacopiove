"""Tests for box sealing state machine and validation rules."""

from datetime import date, datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.services.box_service import BoxService


def _make_db():
    return MagicMock()


def _box(status="DRAFT", **kwargs):
    b = MagicMock()
    b.id = uuid4()
    b.status = status
    b.product_type_id = uuid4()
    b.batch = "L001"
    b.expiry_date = date.today() + timedelta(days=400)
    for k, v in kwargs.items():
        setattr(b, k, v)
    return b


def _pt(category="FOOD", **kwargs):
    pt = MagicMock()
    pt.category = category
    pt.inn_name = "Paracetamol"
    pt.form = "tableta"
    pt.strength = "500mg"
    for k, v in kwargs.items():
        setattr(pt, k, v)
    return pt


CENTER_ID = uuid4()
USER_ID = uuid4()


def _make_service_with(box, pt):
    db = _make_db()
    svc = BoxService(db)
    with (
        patch("app.services.box_service.BoxRepository") as MockBoxRepo,
        patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
    ):
        MockBoxRepo.return_value.find_by_id.return_value = box
        MockPtRepo.return_value.find_by_id.return_value = pt
        MockBoxRepo.return_value.commit = MagicMock()
        yield svc, MockBoxRepo, MockPtRepo


class TestBoxSeal:

    def test_seal_draft_food_box_ok(self):
        box = _box(status="DRAFT")
        pt = _pt(category="FOOD")
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            MockBoxRepo.return_value.commit = MagicMock()
            result = svc.seal(box.id, CENTER_ID, USER_ID)
        assert result.status == "SEALED"
        assert result.sealed_at is not None

    def test_seal_already_sealed_raises(self):
        from fastapi import HTTPException
        box = _box(status="SEALED")
        pt = _pt(category="FOOD")
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            with pytest.raises(HTTPException) as exc_info:
                svc.seal(box.id, CENTER_ID, USER_ID)
        assert exc_info.value.status_code == 400

    def test_seal_rejected_raises(self):
        from fastapi import HTTPException
        box = _box(status="REJECTED")
        pt = _pt(category="FOOD")
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            with pytest.raises(HTTPException) as exc_info:
                svc.seal(box.id, CENTER_ID, USER_ID)
        assert exc_info.value.status_code == 400

    def test_seal_medicine_without_batch_raises(self):
        from fastapi import HTTPException
        box = _box(status="DRAFT", batch=None)
        pt = _pt(category="MEDICINE")
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            with pytest.raises(HTTPException) as exc_info:
                svc.seal(box.id, CENTER_ID, USER_ID)
        assert exc_info.value.status_code == 422

    def test_seal_medicine_without_expiry_raises(self):
        from fastapi import HTTPException
        box = _box(status="DRAFT", expiry_date=None)
        pt = _pt(category="MEDICINE")
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            with pytest.raises(HTTPException) as exc_info:
                svc.seal(box.id, CENTER_ID, USER_ID)
        assert exc_info.value.status_code == 422

    def test_seal_medicine_missing_inn_raises(self):
        from fastapi import HTTPException
        box = _box(status="DRAFT")
        pt = _pt(category="MEDICINE", inn_name=None)
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            with pytest.raises(HTTPException) as exc_info:
                svc.seal(box.id, CENTER_ID, USER_ID)
        assert exc_info.value.status_code == 422

    def test_seal_medicine_ok(self):
        box = _box(status="DRAFT")
        pt = _pt(category="MEDICINE")
        db = _make_db()
        svc = BoxService(db)
        with (
            patch("app.services.box_service.BoxRepository") as MockBoxRepo,
            patch("app.services.box_service.ProductTypeRepository") as MockPtRepo,
        ):
            MockBoxRepo.return_value.find_by_id.return_value = box
            MockPtRepo.return_value.find_by_id.return_value = pt
            MockBoxRepo.return_value.commit = MagicMock()
            result = svc.seal(box.id, CENTER_ID, USER_ID)
        assert result.status == "SEALED"

    def test_box_not_found_raises_404(self):
        from fastapi import HTTPException
        db = _make_db()
        svc = BoxService(db)
        with patch("app.services.box_service.BoxRepository") as MockBoxRepo:
            MockBoxRepo.return_value.find_by_id.return_value = None
            with pytest.raises(HTTPException) as exc_info:
                svc.seal(uuid4(), CENTER_ID, USER_ID)
        assert exc_info.value.status_code == 404

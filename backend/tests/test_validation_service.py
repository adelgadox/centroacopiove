"""Tests for validation_service — business rules from CLAUDE.md §7 (WHO Guidelines)."""

from datetime import date, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.schemas.intake import BoxDraft
from app.services.validation_service import validate_box

_DUMMY_PT_ID = uuid4()


def _pt(**kwargs):
    """Build a minimal mock ProductType."""
    defaults = dict(
        category="MEDICINE",
        is_controlled=False,
        min_shelf_life_days=None,
        inn_name="Paracetamol",
        form="tableta",
        strength="500mg",
    )
    defaults.update(kwargs)
    m = MagicMock()
    for k, v in defaults.items():
        setattr(m, k, v)
    return m


def _box(**kwargs):
    defaults = dict(
        product_type_id=_DUMMY_PT_ID,
        quantity=10,
        unit="tabletas",
        batch="L001",
        expiry_date=date.today() + timedelta(days=400),
        weight_kg=None,
    )
    defaults.update(kwargs)
    return BoxDraft(**defaults)


TODAY = date.today()

# ── Controlled substances ─────────────────────────────────────────────────────

def test_controlled_always_rejected():
    box = _box()
    pt = _pt(is_controlled=True)
    reason = validate_box(box, pt, TODAY)
    assert reason is not None
    assert "controlado" in reason.lower()


# ── Medicine: shelf life ──────────────────────────────────────────────────────

def test_medicine_ok_with_365_days():
    box = _box(expiry_date=TODAY + timedelta(days=365))
    pt = _pt(category="MEDICINE")
    assert validate_box(box, pt, TODAY) is None


def test_medicine_rejected_with_364_days():
    box = _box(expiry_date=TODAY + timedelta(days=364))
    pt = _pt(category="MEDICINE")
    reason = validate_box(box, pt, TODAY)
    assert reason is not None
    assert "vida útil" in reason.lower() or "insuficiente" in reason.lower()


def test_medicine_rejected_without_expiry():
    box = _box(expiry_date=None)
    pt = _pt(category="MEDICINE")
    reason = validate_box(box, pt, TODAY)
    assert reason is not None
    assert "caducidad" in reason.lower()


# ── Medicine: required batch ──────────────────────────────────────────────────

def test_medicine_rejected_without_batch():
    box = _box(batch=None)
    pt = _pt(category="MEDICINE")
    reason = validate_box(box, pt, TODAY)
    assert reason is not None
    assert "lote" in reason.lower()


def test_medicine_ok_with_batch():
    box = _box(batch="L001")
    pt = _pt(category="MEDICINE")
    assert validate_box(box, pt, TODAY) is None


# ── Medicine: missing ProductType required fields ─────────────────────────────

def test_medicine_rejected_missing_inn():
    box = _box()
    pt = _pt(category="MEDICINE", inn_name=None)
    reason = validate_box(box, pt, TODAY)
    assert reason is not None
    assert "inn_name" in reason.lower() or "obligatorio" in reason.lower()


def test_medicine_rejected_missing_form():
    box = _box()
    pt = _pt(category="MEDICINE", form=None)
    reason = validate_box(box, pt, TODAY)
    assert reason is not None


def test_medicine_rejected_missing_strength():
    box = _box()
    pt = _pt(category="MEDICINE", strength=None)
    reason = validate_box(box, pt, TODAY)
    assert reason is not None


# ── Food: shelf life ──────────────────────────────────────────────────────────

def test_food_ok_with_180_days():
    box = _box(expiry_date=TODAY + timedelta(days=180))
    pt = _pt(category="FOOD", inn_name=None, form=None, strength=None)
    assert validate_box(box, pt, TODAY) is None


def test_food_rejected_with_179_days():
    box = _box(expiry_date=TODAY + timedelta(days=179))
    pt = _pt(category="FOOD", inn_name=None, form=None, strength=None)
    reason = validate_box(box, pt, TODAY)
    assert reason is not None


def test_food_rejected_without_expiry():
    box = _box(expiry_date=None)
    pt = _pt(category="FOOD", inn_name=None, form=None, strength=None)
    reason = validate_box(box, pt, TODAY)
    assert reason is not None


# ── Min shelf life override ───────────────────────────────────────────────────

def test_custom_min_shelf_life_override():
    """ProductType.min_shelf_life_days overrides the category default."""
    box = _box(expiry_date=TODAY + timedelta(days=90))
    pt = _pt(category="FOOD", inn_name=None, form=None, strength=None, min_shelf_life_days=30)
    # 90 days > 30 days custom minimum → should pass
    assert validate_box(box, pt, TODAY) is None


# ── Categories without shelf life requirement ─────────────────────────────────

def test_tool_no_expiry_ok():
    box = _box(expiry_date=None, batch=None)
    pt = _pt(category="TOOL", inn_name=None, form=None, strength=None)
    assert validate_box(box, pt, TODAY) is None


def test_medical_supply_no_expiry_ok():
    box = _box(expiry_date=None, batch=None)
    pt = _pt(category="MEDICAL_SUPPLY", inn_name=None, form=None, strength=None)
    assert validate_box(box, pt, TODAY) is None

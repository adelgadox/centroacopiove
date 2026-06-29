"""Tests for Campaign schemas and service logic."""

from datetime import date
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.campaign import CampaignCreate, CampaignUpdate


class TestCampaignCreateSchema:
    def test_minimal_required_fields(self):
        c = CampaignCreate(name="Campaña Venezuela 2026")
        assert c.name == "Campaña Venezuela 2026"
        assert c.destination_country is None
        assert c.start_date is None

    def test_full_fields(self):
        c = CampaignCreate(
            name="Op. Venezuela",
            destination_country="VE",
            description="Terremoto norte de Venezuela",
            start_date=date(2026, 6, 24),
            end_date=date(2026, 12, 31),
        )
        assert c.destination_country == "VE"
        assert c.start_date == date(2026, 6, 24)

    def test_valid_destination_mx(self):
        c = CampaignCreate(name="Test", destination_country="MX")
        assert c.destination_country == "MX"

    def test_invalid_destination_lowercase(self):
        with pytest.raises(ValidationError):
            CampaignCreate(name="Test", destination_country="ve")

    def test_invalid_destination_three_letters(self):
        with pytest.raises(ValidationError):
            CampaignCreate(name="Test", destination_country="VEN")

    def test_empty_name_not_allowed(self):
        with pytest.raises(ValidationError):
            CampaignCreate(name=None)  # type: ignore


class TestCampaignUpdateSchema:
    def test_all_none_ok(self):
        u = CampaignUpdate()
        assert u.name is None
        assert u.is_active is None

    def test_deactivate(self):
        u = CampaignUpdate(is_active=False)
        assert u.is_active is False

    def test_invalid_country_in_update(self):
        with pytest.raises(ValidationError):
            CampaignUpdate(destination_country="usa")

    def test_valid_country_in_update(self):
        u = CampaignUpdate(destination_country="US")
        assert u.destination_country == "US"

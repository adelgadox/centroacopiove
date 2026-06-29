"""Tests for country_code / state_name fields on Center schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.center import CenterCreate, CenterUpdate


class TestCenterCreateGeo:
    def test_valid_country_code(self):
        c = CenterCreate(name="Test", country_code="MX")
        assert c.country_code == "MX"

    def test_valid_country_code_ve(self):
        c = CenterCreate(name="Test", country_code="VE")
        assert c.country_code == "VE"

    def test_country_code_none_ok(self):
        c = CenterCreate(name="Test")
        assert c.country_code is None

    def test_country_code_lowercase_rejected(self):
        with pytest.raises(ValidationError):
            CenterCreate(name="Test", country_code="mx")

    def test_country_code_three_letters_rejected(self):
        with pytest.raises(ValidationError):
            CenterCreate(name="Test", country_code="MEX")

    def test_country_code_one_letter_rejected(self):
        with pytest.raises(ValidationError):
            CenterCreate(name="Test", country_code="M")

    def test_state_name_optional(self):
        c = CenterCreate(name="Test", country_code="MX", state_name="Jalisco")
        assert c.state_name == "Jalisco"

    def test_state_name_none_ok(self):
        c = CenterCreate(name="Test")
        assert c.state_name is None


class TestCenterUpdateGeo:
    def test_update_country_code(self):
        u = CenterUpdate(country_code="US")
        assert u.country_code == "US"

    def test_update_invalid_country_code(self):
        with pytest.raises(ValidationError):
            CenterUpdate(country_code="usa")

    def test_update_state_name(self):
        u = CenterUpdate(state_name="Texas")
        assert u.state_name == "Texas"

    def test_update_all_none_ok(self):
        u = CenterUpdate()
        assert u.country_code is None
        assert u.state_name is None

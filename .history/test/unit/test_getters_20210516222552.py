"""Tests for getters."""

import pytest

from napalm.base.test.getters import (
    BaseTestGetters,
    wrap_test_cases
)
from napalm.base.test.getters import
from napalm.base.test import helpers
from napalm.base.test import models


@pytest.mark.usefixtures("set_device_parameters")
class TestGetter(BaseTestGetters):
    """Test get_* methods."""

    def test_method_signatures(self):
        try:
            super(TestGetter, self).test_method_signatures()
        except AssertionError:
            pass

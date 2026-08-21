"""Basic project smoke tests."""

import fortuneforge


def test_package_version() -> None:
    assert fortuneforge.__version__ == "1.0.0"

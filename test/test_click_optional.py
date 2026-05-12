"""Test that click is optional for library users."""
import builtins
import importlib
import sys

import pytest


@pytest.fixture(autouse=True)
def restore_imported_modules():
    """Keep the simulated missing dependency scoped to each test."""
    original_module = sys.modules.get("x_wr_timezone")
    original_click = sys.modules.get("click")
    yield
    sys.modules.pop("x_wr_timezone", None)
    sys.modules.pop("click", None)
    if original_module is not None:
        sys.modules["x_wr_timezone"] = original_module
    if original_click is not None:
        sys.modules["click"] = original_click


def import_x_wr_timezone_without_click(monkeypatch):
    """Import x_wr_timezone with click hidden from the import system."""
    real_import = builtins.__import__

    def import_without_click(name, *args, **kwargs):
        if name == "click":
            raise ImportError("No module named 'click'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_without_click)
    sys.modules.pop("x_wr_timezone", None)
    sys.modules.pop("click", None)
    return importlib.import_module("x_wr_timezone")


def test_import_without_click(monkeypatch):
    """Importing the library should not require the cli extra."""
    module = import_x_wr_timezone_without_click(monkeypatch)

    assert hasattr(module, "to_standard")


def test_cli_reports_missing_click(monkeypatch):
    """The command should explain how to install its optional dependency."""
    module = import_x_wr_timezone_without_click(monkeypatch)

    with pytest.raises(SystemExit) as exit_info:
        module.main()

    assert "x-wr-timezone[cli]" in str(exit_info.value)

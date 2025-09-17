import pandas as pd
import pytest

from services.sheets import fetch_dashboard_frames


@pytest.fixture
def sample_frames(monkeypatch):
    def fake_loader():
        return {
            "Expenses": pd.DataFrame({"תאריך": pd.to_datetime(["2024-01-01"]), "שקלים": [100]}),
            "Donations": pd.DataFrame({"תאריך": pd.to_datetime(["2024-01-02"]), "שקלים": [200]}),
        }

    monkeypatch.setattr("services.sheets.load_all_data", fake_loader)


def test_fetch_dashboard_frames_populates_known_keys(sample_frames):
    frames = fetch_dashboard_frames()
    assert set(frames.keys()) == {"Expenses", "Donations", "Investors", "Widows"}
    for key in ["Expenses", "Donations", "Investors", "Widows"]:
        assert isinstance(frames[key], pd.DataFrame)
    assert not frames["Expenses"].empty
    assert not frames["Donations"].empty


def test_fetch_dashboard_frames_handles_empty(monkeypatch):
    monkeypatch.setattr("services.sheets.load_all_data", lambda: {})
    frames = fetch_dashboard_frames()
    for frame in frames.values():
        assert isinstance(frame, pd.DataFrame)
        assert frame.empty


def test_fetch_dashboard_frames_handles_exception(monkeypatch):
    def boom():
        raise RuntimeError("boom")

    monkeypatch.setattr("services.sheets.load_all_data", boom)
    frames = fetch_dashboard_frames()
    for frame in frames.values():
        assert frame.empty

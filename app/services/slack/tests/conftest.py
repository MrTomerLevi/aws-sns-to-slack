import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("SLACK_HOOK_URL", "sedric-dev")
    monkeypatch.setenv("SLACK_CHANNEL", "testing-bucket-data")
    monkeypatch.setenv("POWERTOOLS_TRACE_DISABLED", "1")

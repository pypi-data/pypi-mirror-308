import pytest

from src.logger import OmniLog


@pytest.mark.asyncio
async def test_logger_initialization():
    olo = OmniLog(service_name="TestService", db_name="test_omni_log")
    assert olo.service_name == "TestService"
    assert olo.task_id is not None

    assert olo.log(
        log_level="INFO", message="Test log message", context={"key": "value"}
    )

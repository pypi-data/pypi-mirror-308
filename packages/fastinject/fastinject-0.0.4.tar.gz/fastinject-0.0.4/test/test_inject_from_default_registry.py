import logging
from typing import Optional

import pytest

from src.fastinject import Registry, get_default_registry, set_default_registry
from src.fastinject.decorators import inject
from test.objects_for_testing import services, service_configs
from test.objects_for_testing.service_configs import SCDatabaseLogging


def test_inject_from_default_registry():
    """Test example"""
    # 1. Create registry
    registy = Registry(service_configs=[SCDatabaseLogging])
    assert registy is not None
    assert get_default_registry() is not None

    @inject()
    def getlogger(_logger: logging.Logger) -> None:
        assert _logger is not None

    getlogger()


def test_inject_raises_if_module_not_registered_from_default_registry_double():
    """Test example"""
    # 1. Create registry
    registy = Registry(
        service_configs=[
            SCDatabaseLogging,
        ]
    )  # ModuleTimestamper])
    assert registy is not None
    assert get_default_registry() is not None

    @inject()
    def getlogger(ts: services.TimeStamp, logger: logging.Logger) -> None: ...

    with pytest.raises(TypeError):
        getlogger()


def test_injects_none_on_missing_service():
    """Test example"""
    # 1. Create registry
    registy = Registry(service_configs=[SCDatabaseLogging])
    assert registy is not None
    assert get_default_registry() is not None

    @inject()
    def getlogger(_logger: logging.Logger, ts: Optional[services.TimeStamp] = None) -> None:
        assert _logger is not None
        assert ts is None

    getlogger()


def test_imperative():
    reg = get_default_registry()
    assert reg is not None


def test_raises_on_failed_service_init():
    """Test example"""
    # 1. Create registry
    set_default_registry(registry=None)
    registy = Registry(service_configs=[service_configs.SCDatabaseInitFails], auto_validate=False)
    assert registy is not None
    # assert get_default_registry() is not None

    # this will init the services
    assert registy.get(services.DatabaseConnection) is None

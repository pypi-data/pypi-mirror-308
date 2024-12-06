import logging

from src.fastinject import Registry, inject_from
from test.objects_for_testing import service_configs


def test_can_call_with_injection():
    # 1. Create registry
    registry = Registry(service_configs=[service_configs.SCLogging, service_configs.SCDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_both(dbcon: service_configs.DatabaseConfig, _logger: logging.Logger):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
        assert _logger is not None

    registry.call_with_injection(callable=inject_both)


def test_can_call_with_injection_additional_args():
    # 1. Create registry
    registry = Registry(service_configs=[service_configs.SCLogging, service_configs.SCDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_both(dbcon: service_configs.DatabaseConfig, _logger: logging.Logger, name: str):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
        assert _logger is not None
        assert name == "some_name"

    registry.call_with_injection(callable=inject_both, kwargs={"name": "some_name"})

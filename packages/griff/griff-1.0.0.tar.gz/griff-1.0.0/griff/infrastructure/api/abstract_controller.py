from abc import ABC

from injector import singleton

from griff.infrastructure.registry.meta_endpoint_controller_registry import (
    MetaEndpointControllerRegistry,
)
from griff.utils.find_method_bound_to_obj import find_bound_method_to_object


class AbstractEndpointController(ABC, metaclass=MetaEndpointControllerRegistry):
    @singleton
    def __init__(self):
        """
        Auto register endpoint in fastApi router
        """
        endpoint_list = MetaEndpointControllerRegistry.get_endpoint_registry()[
            type(self)
        ]
        self._endpoints = list()
        for endpoint in endpoint_list:
            endpoint_route = MetaEndpointControllerRegistry.get_full_route_for_endpoint(
                controller=self, endpoint=endpoint
            )
            if endpoint_route is None:
                continue
            self._endpoints.append(
                {
                    "route": endpoint_route,
                    "method": endpoint.http_method,
                    "func": find_bound_method_to_object(self, endpoint.endpoint),
                    "return_code": endpoint.http_success_code,
                }
            )

    def get_endpoints(self):
        return self._endpoints

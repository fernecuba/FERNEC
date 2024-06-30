from .main import v1_router
from .health import router as health_router
from .predict import router as predict_router
from .messaging import router as messaging_router


def test_v1_router_includes_routers():
    v1_routes = [route.path for route in v1_router.routes]

    predict_router_routes = [f"/v1{route.path}" for route in predict_router.routes]
    for route in predict_router_routes:
        assert route in v1_routes

    health_router_routes = [f"/v1{route.path}" for route in health_router.routes]
    for route in health_router_routes:
        assert route in v1_routes

    messaging_router_routes = [f"/v1{route.path}" for route in messaging_router.routes]
    for route in messaging_router_routes:
        assert route in v1_routes

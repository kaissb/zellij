# zellij/router.py
import asyncio
from starlette.routing import Route

class Router:
    def __init__(self, app):
        self.app = app

    def add_route(self, path, view, methods=["GET"]):
        if asyncio.iscoroutinefunction(view):
            route = Route(path, view, methods=methods)
            self.app.routes.append(route)
        else:
            raise ValueError("View function must be an asynchronous coroutine")

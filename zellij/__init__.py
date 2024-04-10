# zellij/__init__.py
import yaml
from starlette.applications import Starlette
from .router import Router


class ZellijApp:
    def __init__(self, config_path="config.yaml"):
        self.config = self.load_config(config_path)
        self.app = Starlette(debug=self.config["app"]["debug"])
        self.router = Router(self.app)

    def load_config(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def add_route(self, path, view, methods=["GET"]):
        self.router.add_route(path, view, methods)

    def run(self):
        import uvicorn

        uvicorn.run(
            self.app, host=self.config["app"]["host"], port=self.config["app"]["port"]
        )


__all__ = ["ZellijApp"]

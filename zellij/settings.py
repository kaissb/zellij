# zellij/settings.py
import yaml


def load_config(config_path="settings.yaml"):
    with open(config_path, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg


config = load_config()

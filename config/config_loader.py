import yaml
import os

def load_config(env):
    file_path = os.path.join("config", f"{env}.yaml")
    with open(file_path) as file:
        return yaml.safe_load(file)
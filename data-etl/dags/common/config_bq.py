import yaml
from pathlib import Path

CONFIG_PATH = (
    Path(__file__).resolve().parents[2]
    / "config"
    / "bq_config.yaml"
)


def load_bq_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)

    except Exception as e:
        print("CONFIG ERROR:", e)
        raise
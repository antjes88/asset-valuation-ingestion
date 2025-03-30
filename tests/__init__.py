import os
from src.entrypoints.cli.utils import env_var_loader
import warnings


warnings.filterwarnings("ignore", category=UserWarning)

env_var_loader("tests/.env")

# load sa if applicable
if os.environ.get("SA_JSON"):
    name = "sa.json"
    with open(name, "w") as f:
        f.write(os.environ.get("SA_JSON", ""))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = name

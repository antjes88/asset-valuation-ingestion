import os
from dotenv import load_dotenv
import sys


def env_var_loader(file_name, file_path=None):
    """
    Load environment variables from a specified file using python-dotenv.

    Args:
        file_name (str): The name of the environment file.
        file_path (str, optional): The path to the directory containing the environment file.
    """
    if file_path:
        env_path = os.path.join(file_path, file_name)
    else:
        wd = os.getcwd()
        env_path = os.path.join(wd, file_name)

    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)


# load env vars
env_var_loader("tests/.env")

# load path to get python files
sys.path.append(os.path.join(os.getcwd(), "cloud_function"))

# load sa if applicable
if os.environ.get("SA_JSON"):
    name = "sa.json"
    with open(name, "w") as f:
        f.write(os.environ.get("SA_JSON"))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = name

import click
from src.entrypoints.cli.load_file import (
    load_gcp_file,
    load_local_file,
    load_all_files_from_bucket,
)
from src.utils.env_var_loader import env_var_loader
import warnings


warnings.filterwarnings("ignore", category=UserWarning)


@click.group()
def cli():
    pass


cli.add_command(load_local_file)
cli.add_command(load_gcp_file)
cli.add_command(load_all_files_from_bucket)

if __name__ == "__main__":
    env_var_loader(".env")
    cli()

import click
from src.entrypoints.cli.load_file import (
    load_gcp_file,
    load_local_file,
    load_all_files_from_bucket,
)
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


@click.group()
def cli():
    pass


cli.add_command(load_local_file)
cli.add_command(load_gcp_file)
cli.add_command(load_all_files_from_bucket)

if __name__ == "__main__":
    load_dotenv(dotenv_path=".env", override=True)
    cli()

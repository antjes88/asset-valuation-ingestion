import click
from cli.dummy import dummy


@click.group()
def cli():
    pass


cli.add_command(dummy)

if __name__ == "__main__":
    cli()

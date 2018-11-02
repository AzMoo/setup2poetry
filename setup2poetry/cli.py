import click

from .adapter import PoetryAdapter


@click.command()
@click.argument('package')
@click.argument('output', type=click.File('w'), default='pyproject.toml')
def main(package, output):
    adapter = PoetryAdapter(package)
    adapter.write(output)

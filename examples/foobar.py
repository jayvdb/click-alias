import click
from click_alias import ClickAliasedGroup


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


@cli.command(aliases=['bar', 'baz', 'qux'])
def foo():
    """Run a command."""
    click.echo('foo')


if __name__ == "__main__":
    cli()

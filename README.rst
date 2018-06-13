===========
click-alias
===========

**This is experimental, which is why it's not on PyPI**

Add (multiple) aliases to a click_ group or command.

In your click_ app:

.. code:: python

    import click
    from click_alias import ClickAliasedGroup

    @click.group(cls=ClickAliasedGroup)
    def cli():
        pass

    @cli.command(aliases=['bar', 'baz', 'qux'])
    def foo():
        """Run a command."""
        click.echo('foo')

Will result in:

.. code::

    Usage: cli [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      foo (bar,baz,qux)  Run a command.

.. _click: http://click.pocoo.org/


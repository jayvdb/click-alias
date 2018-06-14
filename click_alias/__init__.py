"""
    Extension for the python ``click`` module
    to provide a group or command with aliases.
"""

import click


class ClickAliasedGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super(ClickAliasedGroup, self).__init__(*args, **kwargs)
        self._commands = {}
        self._aliases = {}

    def command(self, *args, **kwargs):
        aliases = kwargs.pop('aliases', [])
        decorator = super(ClickAliasedGroup, self).command(*args, **kwargs)
        if not aliases:
            return decorator

        def _decorator(f):
            cmd = decorator(f)
            if aliases:
                self._commands[cmd.name] = aliases
                for alias in aliases:
                    self._aliases[alias] = cmd.name
            return cmd

        return _decorator

    def group(self, *args, **kwargs):
        aliases = kwargs.pop('aliases', [])
        decorator = super(ClickAliasedGroup, self).group(*args, **kwargs)
        if not aliases:
            return decorator

        def _decorator(f):
            cmd = decorator(f)
            if aliases:
                self._commands[cmd.name] = aliases
                for alias in aliases:
                    self._aliases[alias] = cmd.name
            return cmd

        return _decorator

    def get_command(self, ctx, cmd_name):
        if cmd_name in self._aliases:
            cmd_name = self._aliases[cmd_name]
        command = super(ClickAliasedGroup, self).get_command(ctx, cmd_name)
        if command:
            return command

    # SYNC_ME: (lb): This is nasty. Click v7 breaks the first version of this
    # function (the only I copied from some rando's GitHub, and then uploaded
    # to PyPI). To make it play nice, ideally, we'd break up Click's base
    # function, MultiCommand.format_commands, into pieces, so that we could
    # just add 3 lines of new code and do nothing else. But that function is
    # long, and we want to add a few lines to the middle of it; so we need to
    # duplicate the whole function. So this block is 95% copy-paste, yuck!
    def format_commands(self, ctx, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            # CLICK-ALIAS: THIS IS THE ONLY 3 lines IN THIS FUNC THAT ARE UNIQUE.
            #   The rest of this function is a copy of the base class's function.
            if subcommand in self._commands:
                aliases = ','.join(sorted(self._commands[subcommand]))
                subcommand = '{0} ({1})'.format(subcommand, aliases)

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section('Commands'):
                    formatter.write_dl(rows)


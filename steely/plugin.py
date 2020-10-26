import logging

from collections import namedtuple
from enum import Enum


class CommandPartType(Enum):
    # A subcommand, eg. the token "set" in "/np set <username>".
    SUBCOMMAND = 1
    # A required argument to the command, eg. "<username>" in "/np set
    # <username>". Required arguments are denoted by some token surrounded by
    # <pointy brackets>. In this example, that CommandPart will have the name
    # "username".
    REQUIRED_ARGUMENT = 2
    # An optional argument to the command, eg. the token "[username]" in "/np
    # [username]". Optional arguments are denoted by some token surrounded by
    # [square brackets]. In this example, that CommandPart will have the name
    # "username".
    OPTIONAL_ARGUMENT = 3

# A single possible match of a PluginCommand for some command string from a
# user.
CommandMatch = namedtuple('CommandMatch', [
    # An int with the number of tokens consumed.
    'num_parts',
    # An int with some value of the match. Stricter matches (eg.
    # SUBCOMMAND > REQUIRED_ARGUMENT, REQUIRED_ARGUMENT > OPTIONAL_ARGUMENT) add
    # a higher value to this match.
    'value',
    # An int containing the number of characters of prefix of the given command
    # were matched by this PluginCommand.
    'str_len',
    # A dict {arg_name: arg_value} of args parsed from this command call.
    'args'
])


class PluginCommand:

    class CommandPart:
        # One specific token in a command string declaration. This has two
        # fields:
        # .name contains the name of the argument, or the subcommand string, if
        # it is a subcommand part and not an argument.
        # .type is a CommandPartType specifying the type of this command part.

        def __init__(self, _str):
            if not len(_str):
                raise ValueError('Cannot define arg for empty string: ' + _str)
            self._str = _str
            if _str[0] == '<' and _str[-1] == '>':
                # Required arg.
                self.type = CommandPartType.REQUIRED_ARGUMENT
                self.name = _str[1:-1]
            elif _str[0] == '[' and _str[-1] == ']':
                # Optional arg
                self.type = CommandPartType.OPTIONAL_ARGUMENT
                self.name = _str[1:-1]
            else:
                self.type = CommandPartType.SUBCOMMAND
                self.name = _str

    def __init__(self, command, func):
        self.command = command
        self.func = func
        self.command_parts = self._parse_defined_command_parts(command)

    def _parse_defined_command_parts(self, command_str):
        parts = command_str.split(' ')
        return [PluginCommand.CommandPart(part) for part in parts]

    def _parse_command_call(self, expected_command_parts, called_command_parts):
        # Returns a CommandMatch tuple for the given expected command parts and
        # actual given command parts.
        parsed_args = {}
        i = 0
        str_match_len = 0

        # match_value is an arbitrary numeric scoring for how nice this match is.
        # It allows us to differentiate between "/np help" being a call to
        # "/np help", or a call to "/np [username]" where username = "help".
        # The first case, with an exact string match, would have a higher
        # match_value.
        match_value = 0
        while i < len(expected_command_parts) and i < len(called_command_parts):
            expected_part = expected_command_parts[i]
            if expected_part.type is CommandPartType.SUBCOMMAND:
                # Required str, must match exactly.
                if called_command_parts[i] == expected_part.name:
                    str_match_len += len(called_command_parts[i])
                    i += 1
                    match_value += 5
                    continue
                else:
                    # Expected some specific str, got something else, abort.
                    return CommandMatch(0, 0, 0, {})

            elif expected_part.type is CommandPartType.REQUIRED_ARGUMENT:
                parsed_args[expected_part.name] = called_command_parts[i]
                str_match_len += len(called_command_parts[i])
                i += 1
                match_value += 3

            elif expected_part.type is CommandPartType.OPTIONAL_ARGUMENT:
                # If the expected command is "/help [search_str] <topic>" to
                # yield only the part of the helpstring for "topic" relevant to
                # "search_str", and the called command is "/help jamiroquai",
                # then decide if we should count "jamiroquai" as a search_str
                # or as a topic for a better overall match.
                # We do this by trying both options, and seeing which has a
                # better score, erring on the side of over-matching.
                logging.debug(
                    'Trying to match part "%s" against optional command "%s".',
                    called_command_parts[i], expected_command_parts[i].name)

                match_with_arg = self._parse_command_call(
                    expected_command_parts[i + 1:],
                    called_command_parts[i + 1:])
                match_with_arg.args[expected_command_parts[
                    i].name] = called_command_parts[i]

                match_with_arg = CommandMatch(match_with_arg.num_parts,
                                              match_with_arg.value + 1,
                                              match_with_arg.str_len +
                                              len(called_command_parts[i]),
                                              match_with_arg.args)

                match_without_arg = self._parse_command_call(
                    expected_command_parts[i + 1:], called_command_parts[i:])

                # Choose whether matching or not matching this optional argument
                # creates a better overall match for the string...
                best_match = match_without_arg
                if match_with_arg.num_parts >= match_without_arg.num_parts:
                    logging.debug(
                        'Matching "%s" against "%s" is better than not.',
                        called_command_parts[i], expected_command_parts[i].name)
                    best_match = match_with_arg

                # We must add 1 here because the optional arg was matched either
                # way, as it is optional... So 'i' can progress to the next
                # expected part.
                i += best_match.num_parts + 1
                match_value += best_match.value
                parsed_args.update(best_match.args)
                str_match_len += best_match.str_len

        # If we reached the end of the input string and there is still something
        # expected that _must_ be matched, then this avenue is useless, return
        # no match.
        if i < len(expected_command_parts):
            for other_expected_part in expected_command_parts[i:]:
                if other_expected_part.type in [
                        CommandPartType.REQUIRED_ARGUMENT,
                        CommandPartType.SUBCOMMAND]:
                    logging.debug(
                        'Reached end of command call str, ' +
                        'but no match found for "{}".'.format(
                            other_expected_part.name))
                    return CommandMatch(0, 0, 0, {})

        # We don't want i to ever be greater than len(expected_command_parts)...
        # Not that this should ever happen.
        i = min(i, len(expected_command_parts))

        logging.debug('Matched {} parts for call "{}" in plugin "{}"'.format(
            i, called_command_parts, self.command))
        return CommandMatch(i, match_value, str_match_len, parsed_args)

    def get_best_match(self, called_command_parts):
        # Returns the best possible CommandMatch for this argument.
        # There may be more than one possible match, depending on whether or not
        # optional arguments are consumed, so this will find the best possible
        # one.
        return self._parse_command_call(self.command_parts,
                                        called_command_parts)


class PluginManager:
    _command_listeners = []  # A list of PluginCommands.
    _passive_listeners = []  # A list of plain funcs.

    @classmethod
    def get_passive_listeners(cls):
        return cls._passive_listeners

    @classmethod
    def get_listener_for_command(cls, command):
        # Assumes "command" does not start with "/". Eg. for "/np top 7day",
        # "command" would be "np top 7day" returns longest matching command and
        # a func to be called against "command".

        command = command.lower().strip()
        logging.debug('Finding longest match for "/{}".'.format(command))
        logging.debug('Active listeners: %s', ','.join(
            c.command for c in cls._command_listeners))

        command_parts = command.split(' ')

        best_match = CommandMatch(0, 0, 0, {})
        best_match_plugin = None

        for plugin_command in cls._command_listeners:
            command_match = plugin_command.get_best_match(command_parts)
            if ((command_match.num_parts > best_match.num_parts) or
                (command_match.num_parts == best_match.num_parts and
                    command_match.value > best_match.value)):
                best_match = command_match
                best_match_plugin = plugin_command

        if best_match_plugin is None:
            logging.info(
                'No best matching plugin found for call "{}"'.format(command))
            return None, None, None

        # The "+ best_match_num_parts - 1" part of this is required to account
        # for the spaces between command parts that are matched but never added
        # anywhere before.
        total_str_match_len = best_match.str_len + best_match.num_parts - 1

        logging.debug(
            'Best matching plugin for call "{}" is "{}", with args: {}'.format(
                command, best_match_plugin.command, best_match.args))
        logging.debug('This matches {} parts, with prefix substr "{}".'.format(
            best_match.num_parts, command[:total_str_match_len]))
        return command[:total_str_match_len], best_match_plugin.func, best_match.args

    @classmethod
    def add_passive_listener(cls, func):
        cls._passive_listeners.append(func)

    @classmethod
    def add_listener_for_command(cls, command, func):
        cls._command_listeners.append(PluginCommand(command, func))

    @staticmethod
    def load_plugins():
        import plugins.letterboxd.main
        import plugins.intern.main
        import plugins.corona.main
        import plugins.bible.main
        

class Plugin:
    """A class containing one Steely plugin.

    A plugin can be created by simply calling this class' constructor, eg:

    plugin = Plugin(name='my plugin', author='steely', help='instructions here')

    This plugin can then be configured to listen for specific commands and
    respond to them. Eg. the following decorated function will listen for any
    command of the form "/bazinga". Any time a command matching that pattern is
    sent to a chat the bot is active in, the bazinga() function will be
    triggered.

    @plugin.listen(command='bazinga')
    def bazinga(bot, message, ..., **kwargs):
        bot.sendMessage(message="Bazinga!", ...)

    It is also possible to add more specific patterns to listen for. Arguments
    that the command needs can be declared here, and they will be automatically
    parsed from the command call and added as a keyword argument the function
    receives. The remaining part of the command call, which is not consumed as
    one of the subcommands or arguments, will be in the 'message' argument to
    the decorated function.

    @plugin.listen(command='shout insult [nickname] <target_id>')
    def shout_insult(bot, message, ..., **kwargs):
        nickname = kwargs['nickname']
        insult = 'Hey, {}! _{}_'.format(nickname, message)
        target = kwargs['target_id']
        bot.sendMessage(insult, thread_id=target, ...)

    The plugin manager will try to match the command call to the most specific
    declared matcher. Eg. "/np help" will match
    @plugin.listen(command='np help')
    and not
    @plugin.listen(command='np [username]')
    when both are defined.

    Subcommands required to be included literally (eg. "set" in "/np set") can
    be included inline in the command matcher string: A matcher for
    "/linden invest" would simply be @plugin.listen(command='linden invest')

    Optional arguments can be included in the string surrounded by
    [square brackets]. Eg. @plugin.listen(command='/np [username]')

    Required arguments can be included surrounded by <angle brackets>. Eg.
    @plugin.listen(command='/roll <dice_string>')

    All patterns (subcommands or arguments) are assumed to be single tokens (ie.
    single words) in a single-space-delimited string.

    If no 'command' argument is given to @plugin.listen(), the function will be
    considered a passive listener, and will be triggered for every message sent
    to a channel the bot is active in. Eg.:

    @plugin.listen()
    def respond_to_swearwords(bot, message, ..., **kwargs):
        if 'heck' in message:
            bot.sendMessage('this is a christian server!', ...)

    If a plugin has some operations it needs to do on program startup, then
    those can be performed in a single function annotated by @plugin.setup().
    If this function returns any value, or raises any exception, then it is
    acknowledged that there was some error in setting up this plugin, and the
    command matchers associated with it are ignored. This allows a plugin to be
    disabled at startup and a warning presented to the admin if some required
    dependency is not present, instead of the plugin failing on every message
    at runtime.
    """

    def __init__(self, name, author, help):
        self.name = name
        self.author = author
        self.help = help
        # .active decides whether the plugin is available to be used. This may
        # be false if plugin.setup() fails for some reason.
        self.active = True
        self.commands = []

    def setup(self):
        # TODO(iandioch): Right now, this decorator must be run like the
        # following:
        # @setup()
        # def setup_func():
        #   ...
        #
        # However, it should also be possible to run it without the brackets
        # after @setup, as a naked decorator.
        def wrapper(func):
            try:
                result = func()
                if result is not None:
                    logging.warning(
                        'Received error while running setup for plugin "{}":\n{}.'.format(
                            self.name, result))
                    self.active = False
            except Exception as e:
                logging.error(
                    'Error thrown while running setup for plugin "{}":\n{}.'.format(
                        self.name, e))
                self.active = False
            return func

        # TODO(iandioch): Add the helpstring so that '/help name' might work.
        # TODO(iandioch): Consider that someone shouldn't have to repeat the
        # same root command for all different @plugin.listen() methods in that
        # plugin.
        return wrapper

    def listen(self, command=None):
        # TODO(iandioch): Make it possible to run this as a naked decorator for
        # plugins that are passively listening.
        if not self.active:
            logging.warning(
                'Tried to set up listener "{}" for plugin "{}", but plugin is not active.'.format(
                    command, self.name))
            # Return a do-nothing decorator, as we don't want to register this
            # command.
            return lambda _: None

        logging.debug('Adding command "{}" to plugin "{}" by "{}".'.format(
            command, self.name, self.author))
        # TODO(iandioch): Add functools.wraps() to update __name__, etc.

        def register_listener(func):
            if command is None:
                PluginManager.add_passive_listener(func)
            else:
                PluginManager.add_listener_for_command(command, func)

            return func

        if command is not None:
            logging.debug('Adding command {} to list for plugin {}'.format(
                command, self.name))
            self.commands.append(command)

        return register_listener


def create_plugin(name=None, author=None, help=None):
    return Plugin(name, author, help)

if __name__ == '__main__':
    PluginManager.load_plugins()

class PluginManager:
    _command_listeners = {}
    _passive_listeners = []

    @classmethod
    def get_passive_listeners(cls):
        return cls._passive_listeners

    @classmethod
    def get_listener_for_command(cls, command):
        # assumes "command" does not start with "/". Eg., for "/np top 7day", "command" would be "np top 7day"
        # returns longest matching command and a func to be called against "command"

        print('Finding longest match for "/{}".'.format(command))
        print('Active listeners:', ', '.join(cls._command_listeners.keys()))
        longest_matching_listener = None
        longest_match = 0
        for command_listener in cls._command_listeners:
            if command.startswith(command_listener):
                if len(command_listener) > longest_match:
                    longest_match = len(command_listener)
                    longest_matching_listener = command_listener
        if longest_matching_listener is None:
            return None, None
        return longest_matching_listener, cls._command_listeners[longest_matching_listener]

    @classmethod
    def add_passive_listener(cls, func):
        cls._passive_listeners.append(func)

    @classmethod
    def add_listener_for_command(cls, command, func):
        if command in cls._command_listeners:
            raise KeyError('Tried to add listener for command "{}", but one already exists.'.format(command))
        cls._command_listeners[command] = func

    @staticmethod
    def load_plugins():
        import plugins.letterboxd.main


class Plugin:
    def __init__(self, name, author, help):
        self.name = name
        self.author = author
        self.help = help
        # .active decides whether the plugin is available to be used.
        self.active = True

    def setup(self):
        # TODO(iandioch): Right now, this decorator must be run like the following:
        # @setup()
        # def setup_func():
        #   ...
        # 
        # However, it should also be possible to run it without the brackets after @setup,
        # as a naked decorator.
        def wrapper(func):
            try:
                result = func()
                if result is not None:
                    print('Received error while running setup for plugin "{}":\n{}.'.format(self.name, result)) 
                    print(self.name)
                    self.active = False
            except Exception as e:
                print('Error thrown while running setup for plugin "{}":\n{}.'.format(self.name, e))
                self.active = False
            return func


        print('active?', self.active)
        #TODO(iandioch): Add the helpstring so that '/help name' might work.
        #TODO(iandioch): Consider the fact that "name" and the specific listed commands might be different.
        #TODO(iandioch): Consider that someone shouldn't have to repeat the same root command for all different @plugin.listen() methods in that plugin.
        return wrapper 

    def listen(self, command=None):
        # TODO(iandioch): Make it possible to run this as a naked decorator for plugins that are passively listening.
        if not self.active:
            print('Tried to set up listener "{}" for plugin "{}", but plugin is not active.'.format(command, self.name))
            # Return a do-nothing decorator, as we don't want to register this command.
            return lambda _: None

        print('Adding command "{}" to plugin "{}" by "{}".'.format(command, self.name, self.author))
        #TODO(iandioch): Add functools.wraps() to update __name__, etc.
        def register_listener(func):
            if command is None:
                PluginManager.add_passive_listener(func)
            else:
                PluginManager.add_listener_for_command(command, func)

            return func
        return register_listener 


def create_plugin(name=None, author=None, help=None):
    return Plugin(name, author, help)

if __name__ == '__main__':
    PluginManager.load_plugins()

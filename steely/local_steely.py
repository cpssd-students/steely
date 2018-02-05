import argparse
from utils import scan_plugins_dir, load_plugin

class FBChatMessageMock:
    def __init__(self, message):
        self.text = message


class FBChatMock:
    def __init__(self, prev_messages):
        # List of messages, oldest to newest.
        # This list will be updated with new messages so anything holding a 
        # reference to it will be up to date.
        self.prev_mes = prev_messages
        # This is a seperate list for isolating the output of the plugin.
        self.output_mes = []

    def fetchThreadMessages(self, thread_id, limit):
        return [FBChatMessageMock(m) for m in self.prev_mes[-limit:]][::-1]

    def sendMessage(self, mess, thread_id, thread_type):
        self.output_mes.append(mess)
        self.prev_mes.append(mess)


class SteelyREPL:
    def __init__(self, plugins, prefix='.', author_id="test_author"):
        self._plugins = {
                prefix + p.COMMAND: p for p in plugins if p.COMMAND is not None
        }
        self._all_message_plugins = [p for p in plugins if p.COMMAND is None]
        self._message_list = []
        self._author_id = author_id

    def _exec_plugin(self, plugin, message):
        bot = FBChatMock(self._message_list)
        plugin.main(bot, self._author_id, message,
                    thread_id='test_thread', thread_type='test_thread_type')
        return bot.output_mes

    def _exec_message(self, message):
        plugin_name, *arg = message.split(maxsplit=1)
        arg_str = arg[0] if arg else ''
        if plugin_name in self._plugins:
            yield from self._exec_plugin(self._plugins[plugin_name], arg_str)
            return

        for plugin in self._all_message_plugins:
            yield from self._exec_plugin(plugin, message)

    def _run_noguard(self):
        while True:
            message = input(">>> ")
            self._message_list.append(message)
            for out_m in self._exec_message(message):
                print(out_m)
    
    def run(self):
        try:
            return self._run_noguard()
        except (KeyboardInterrupt, EOFError) as e:
            print()  # Newline needed for pretty exit.
            pass


def get_args():
    parser = argparse.ArgumentParser(
            description=(
                "A plugin runner for steely designed for manual "
                "testing. It supports basic FBChat operations and can load "
                "multiple plugins at once. By default it will attempt to "
                "load ALL plugins but I recommend against doing this"))
    parser.add_argument(
            "-p",
            nargs="+",
            help="A list of plugin filenames to load. E.g. -p b.py box.py")
    parser.add_argument(
            "--plugin-dir",
            default="plugins",
            help="The directory to look for plugins in")
    return parser.parse_args()

def load_plugins(plist, pdir):
    """
    Given a list of plugin filenames return the loaded modules.
    If plist is None then return all plugins found.
    """
    for filename, path in scan_plugins_dir(pdir):
        if plist is None or filename in plist:
            yield load_plugin(filename, path)

def main():
    args = get_args()
    plugins = load_plugins(args.p, args.plugin_dir)
    repl = SteelyREPL(plugins)
    repl.run()

if __name__ == '__main__':
    main()

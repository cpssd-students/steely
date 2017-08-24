import os
import imp


def list_plugins():
    for file in os.listdir('plugins'):
        if file.startswith("_"):
            continue
        elif not file.endswith(".py"):
            continue
        plugin_path = os.path.join('plugins', file)
        yield imp.load_source(file, plugin_path)

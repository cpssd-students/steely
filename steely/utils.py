import os
import imp


def scan_plugins_dir(plugins_dir='plugins'):
    """Scan the given dir for files matching the spec for plugin files"""
    for plugin_file in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_file)
        if (not plugin_file.startswith('_') and
            plugin_file.endswith('.py') and
                os.path.isfile(plugin_path)):

            yield plugin_file, plugin_path


def load_plugin(filename, path):
    return imp.load_source(filename, path)


def list_plugins():
    for plugin_file, plugin_path in scan_plugins_dir():
        yield load_plugin(plugin_file, plugin_path)

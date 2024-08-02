import os
import sys
import xdg.BaseDirectory

def sample_path() -> str:
    return os.path.join(os.path.split(__file__)[0], "config.py.sample")

def get_config(directory, module):
    sys.path.append(directory)
    try:
        return __import__(module)
    except ModuleNotFoundError:
        print(f'{module}.py not found in {directory}/', file=sys.stderr)
        print(f'''you might fix this in the following way:\n
  mkdir -p {directory}
  cp {sample_path()} {directory}/{module}.py
  vim {directory}/{module}.py
        ''', file=sys.stderr)
        sys.exit(1)

# dir
DATA_DIR = xdg.BaseDirectory.save_data_path('steely')
CONFIG_DIR = xdg.BaseDirectory.save_config_path('steely')
DB_DIR = os.path.join(DATA_DIR, 'databases')
LOG_DIR = os.path.join(DATA_DIR, 'logs')

# config
CONFIG = get_config(CONFIG_DIR, 'config')

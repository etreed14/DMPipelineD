import toml
from pathlib import Path

SETTINGS_FILE = Path(__file__).with_name('settings.toml')
settings = toml.loads(SETTINGS_FILE.read_text(encoding='utf-8'))

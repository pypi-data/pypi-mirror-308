from pathlib import Path

from platformdirs import user_cache_dir

APP_NAME: str = 'DotKeeper'
APP_AUTHOR: str = 'Alchemyst0x'
APP_VERSION: str = '0.1.0-alpha1'

FILE_MODE: int = 0o0600
DIR_MODE: int = 0o0700

DOTKEEPER_CACHE: Path = Path(user_cache_dir())

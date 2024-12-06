from typing import Any

from dotkeeper.utils.common import ensure_str_sequence


class DotKeeperError(Exception):
    """Base `Exception` class from which all DotKeeper application errors inherit."""

    def __init__(self, msg: str | list[str] = '', *args: Any) -> None:
        msg = ' '.join(s for s in [*ensure_str_sequence(msg), *ensure_str_sequence(list(args))])
        super().__init__(msg)


class ExecutableNotFoundError(DotKeeperError, FileNotFoundError):
    """Unable to locate executable for command."""

    def __init__(self, exe: str, stderr: str = '', *args: Any) -> None:
        msg = f"Unable to locate executable '{exe}'. Please ensure PATH is set correctly."
        if stderr:
            msg += f"\nOutput on stderr from shell command `which {exe}`: '{stderr}'"
        super().__init__(msg, *args)

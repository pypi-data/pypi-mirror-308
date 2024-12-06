import os
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypeGuard

from dotenv import load_dotenv

from dotkeeper.constants import DIR_MODE, FILE_MODE

load_dotenv()


def is_sequence(obj: Any) -> TypeGuard[Sequence[Any]]:
    return isinstance(obj, Sequence) and not isinstance(obj, str | bytes | bytearray | memoryview)


def ensure_str_sequence(obj: Any) -> Sequence[str]:
    return [str(v).strip() for v in obj] if is_sequence(obj) else [str(obj).strip()]


def expand_path(path: str | Path, *, resolve: bool = False, strict: bool = False) -> Path:
    expanded = Path(os.path.expandvars(str(path))).expanduser()
    return expanded.resolve(strict=strict) if resolve else expanded


def resolve_path(path: str | Path, *, strict: bool = False) -> Path | None:
    try:
        return expand_path(path, resolve=True, strict=strict)
    except Exception:
        return None


def dir_path_from_env(
    var: str,
    *,
    dir_mode: int = DIR_MODE,
    resolve: bool = False,
    ensure: bool = False,
) -> Path | None:
    if (str_path := os.getenv(var)) is not None:
        path = expand_path(str_path)
        if ensure and not path.exists():
            path.mkdir(mode=dir_mode, parents=True, exist_ok=True)
        return path.resolve() if resolve else path
    return None


def file_path_from_env(
    var: str,
    *,
    file_mode: int = FILE_MODE,
    dir_mode: int = DIR_MODE,
    resolve: bool = False,
    ensure: bool = False,
) -> Path | None:
    if (str_path := os.getenv(var)) is not None:
        path = expand_path(str_path)
        if ensure and not path.exists():
            if not path.parent.exists():
                path.mkdir(mode=dir_mode, parents=True, exist_ok=True)
            path.touch(mode=file_mode, exist_ok=True)
        return path.resolve() if resolve else path
    return None

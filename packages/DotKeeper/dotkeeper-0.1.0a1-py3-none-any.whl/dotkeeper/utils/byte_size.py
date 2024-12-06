import re

BYTE_SIZE_MAP: dict[str, int | float] = {
    'b': 1,
    'kb': 10**3,
    'mb': 10**6,
    'gb': 10**9,
    'tb': 10**12,
    'pb': 10**15,
    'eb': 10**18,
    'kib': 2**10,
    'mib': 2**20,
    'gib': 2**30,
    'tib': 2**40,
    'pib': 2**50,
    'eib': 2**60,
    'bit': 1 / 8,
    'kbit': 10**3 / 8,
    'mbit': 10**6 / 8,
    'gbit': 10**9 / 8,
    'tbit': 10**12 / 8,
    'pbit': 10**15 / 8,
    'ebit': 10**18 / 8,
    'kibit': 2**10 / 8,
    'mibit': 2**20 / 8,
    'gibit': 2**30 / 8,
    'tibit': 2**40 / 8,
    'pibit': 2**50 / 8,
    'eibit': 2**60 / 8,
}

BYTE_SIZE_MAP.update({k.lower()[0]: v for k, v in BYTE_SIZE_MAP.items() if 'i' not in k})
BYTE_SIZE_RE = re.compile(r'^\s*(\d*\.?\d+)\s*(\w+)?', re.IGNORECASE)


def from_human_readable(str_size: str) -> int:
    """Convert a human-readable byte size string into its integer counterpart.

    Parameters
    ----------
    str_size : str
        The human-readable byte size string to be converted.

    Returns
    -------
    int
        The converted byte size as an integer value.

    Raises
    ------
    ValueError
        If the input string or unit cannot be parsed.
    """

    str_match = BYTE_SIZE_RE.match(str_size.strip())
    if str_match is None:
        raise ValueError(f"Invalid byte size string: '{str_size}'")

    scalar, unit = str_match.groups()
    if unit is None:
        unit = 'b'

    try:
        multiplier = BYTE_SIZE_MAP[unit.lower()]
    except KeyError as exc:
        raise ValueError(f"Invalid byte size unit: '{unit}'") from exc

    return int(float(scalar) * multiplier)


def to_human_readable(int_size: int, *, decimal: bool = False, separator: str = '') -> str:
    """Convert an integer byte size value into its human-readable string counterpart.

    Parameters
    ----------
    int_size : int
        The byte size as an integer.
    decimal : bool, optional
        If True, use decimal prefixes (`'KB'`, `'MB'`) rather than, e.g., `'KiB'`, `'MiB'`.
        Default is False.
    separator : str, optional
        The separator to use between the number and the size unit. Default is `''`.

    Returns
    -------
    str
        The human-readable byte size string.
    """

    if decimal:
        divisor = 1000
        units = 'B', 'KB', 'MB', 'GB', 'TB', 'PB'
        final_unit = 'EB'
    else:
        divisor = 1024
        units = 'B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB'
        final_unit = 'EiB'

    num = float(int_size)
    for unit in units:
        if abs(num) < divisor:
            if unit == 'B':
                return f'{num:0.0f}{separator}{unit}'
            return f'{num:0.1f}{separator}{unit}'
        num /= divisor

    return f'{num:0.1f}{separator}{final_unit}'


def convert_int_size(int_size: int, unit: str) -> float:
    """Convert an integer byte size value into a float value in the specified unit.

    Parameters
    ----------
    int_size : int
        The byte size as an integer.
    unit : str
        The unit to convert the byte size to (e.g., `GiB`, `KB`, etc.).

    Returns
    -------
    float
        The converted byte size represented as a float value in the specified unit.

    Raises
    ------
    ValueError
        If the unit is unknown.
    """

    try:
        unit_div = BYTE_SIZE_MAP[unit.lower()]
    except KeyError as exc:
        raise ValueError(f"Invalid byte size unit: '{unit}'") from exc

    return int_size / unit_div

__all__ = ("add_one", "_update")


import subprocess

_updated_packages: set[str] = set()


def add_three(number: float) -> float:
    return number + 3


def add_one(number: float) -> float:
    """Increment number by `1`.

    - `numer` can be `int` or `float`.
    - adkfajfl. $\\pi$

    Args:
        number: Value to increment.

    Returns:
        Value incremented by `1`.

    Examples:
        >>> add_one(1)
        2

        >>> add_one(3.14)
        4.14
    """
    return number + 1


def _update(package: str | list[str] | tuple[str, ...], *, t: int | None = None) -> None:
    """Install latest version(s) of package(s) with `uv`.

    - `uv` is implicitly updated first because the update process is fast.

    Args:
        package: Name(s) of the package(s) to update.
        t: Timeout in seconds for each package update. No timeout if `None`.

    Examples:
        >>> _update('tiktoken')

        >>> _update(['numpy', 'scipy'])
    """

    _update_uv()

    for pkg in (package,) if isinstance(package, str) else package:
        if pkg in _updated_packages:
            continue
        try:
            result = subprocess.run(
                ("uv", "pip", "install", "--system", "-U", pkg),
                capture_output=True,
                encoding="utf-8",
                timeout=t,
            )
        except subprocess.TimeoutExpired as exc:
            print(exc)
        else:
            if result.returncode != 0:
                print(result.stderr, end="")
            else:
                _updated_packages.add(pkg)


def _update_uv() -> None:
    if "uv" in _updated_packages:
        return

    try:
        result = subprocess.run(
            ("uv", "pip", "install", "--system", "-Uq", "uv"),
            capture_output=True,
            encoding="utf-8",
            timeout=60,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")
        else:
            _updated_packages.add("uv")

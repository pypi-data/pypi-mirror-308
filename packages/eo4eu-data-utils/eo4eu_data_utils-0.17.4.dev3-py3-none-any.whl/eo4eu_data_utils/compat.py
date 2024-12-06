try:
    from typing import Self, Any, Callable, Iterator, List, Dict
except Exception:
    from typing_extensions import Self, Any, Callable, Iterator, List, Dict


def _get_import_error(name: str, submodule: str) -> str:
    return (f"{name} is not included in the base install of eo4eu-data-utils. " +
            f"Please import using eo4eu-data-utils[{submodule}] or eo4eu-data-utils[full]")

"""verify_imports.py - Script to check import validity across the project.
Ensures that all modules and packages can be imported without errors.
Run this before pytest to confirm your environment setup is correct.

Usage:
    python scripts/verify_imports.py
"""

import importlib
import pkgutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"


def discover_modules(base_path: Path):
    """Recursively discover Python modules in a given base path."""
    sys.path.insert(0, str(base_path))
    for module_info in pkgutil.walk_packages([str(base_path)], prefix=""):
        yield module_info.name


def verify_imports():
    """Try importing all discovered modules and report results."""
    print(f"Verifying imports in: {SRC_DIR}\n")
    all_modules = list(discover_modules(SRC_DIR))

    success, failures = [], []

    for module_name in all_modules:
        try:
            importlib.import_module(module_name)
            success.append(module_name)
        except Exception as e:
            failures.append((module_name, str(e)))

    print(f"Successfully imported {len(success)} modules.")
    if failures:
        print(f"\n{len(failures)} import errors detected:")
        for name, err in failures:
            print(f"  [FAIL] {name}: {err}")
    else:
        print("\n✅ All imports succeeded.")


if __name__ == "__main__":
    verify_imports()

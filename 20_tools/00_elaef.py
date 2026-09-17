#!/usr/bin/env python3
"""Compatibility bridge for existing ELAEF installations."""
import importlib.util
from pathlib import Path
import sys
_spec = importlib.util.spec_from_file_location("eagos_compat_core", Path(__file__).with_name("00_eagos.py"))
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)
globals().update({name: value for name, value in vars(_core).items() if not name.startswith("_")})
if __name__ == "__main__":
    sys.exit(_core.main())

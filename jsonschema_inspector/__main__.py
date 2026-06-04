#!/usr/bin/env python3
"""
Entry point for python -m jsonschema_inspector
"""

from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())

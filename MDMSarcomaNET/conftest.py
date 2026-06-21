"""Pytest konfigurácia — zabezpečí, že balík `mdmsarcnet` je importovateľný."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

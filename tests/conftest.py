import os
import sys
from pathlib import Path


# Ensure project root is importable so `import bot` works when running pytest
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure TOKEN is available for pydantic Settings during imports
os.environ.setdefault("TOKEN", "TEST_TOKEN")



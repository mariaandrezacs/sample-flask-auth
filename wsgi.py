import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from sample_flask_auth import create_app  # noqa: E402

app = create_app()

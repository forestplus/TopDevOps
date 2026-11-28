#!/usr/bin/env python3
from pathlib import Path
import base64
parts = sorted(Path('scripts/exp_b64').glob('*.b64'))
data = ''.join(p.read_text() for p in parts)
Path('scripts/upgrade_experience_cards.py').write_bytes(base64.b64decode(data))
print('decoded ok')

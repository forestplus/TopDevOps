#!/usr/bin/env python3
from pathlib import Path
import base64, gzip
parts_dir = Path("scripts")
full_parts = sorted(parts_dir.glob("idx_exp_full_part_*.b64"))
if full_parts:
    data = "".join(p.read_text().strip() for p in full_parts)
elif (parts_dir / "idx_exp_full.b64").exists():
    data = (parts_dir / "idx_exp_full.b64").read_text().strip()
else:
    parts = sorted(Path("scripts/idx_exp_b64").glob("*.b64"))
    assert parts, "no b64 parts"
    data = "".join(p.read_text().strip() for p in parts)
html = gzip.decompress(base64.b64decode(data))
Path("index.html").write_bytes(html)
text = html.decode("utf-8")
assert "NDA (ОАЭ, Дубай)" in text
assert text.count('class="timeline-item"') == 10
print("index.html written", len(html))

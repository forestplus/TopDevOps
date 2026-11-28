#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
t = Path('index.html').read_text(encoding='utf-8')
t2 = t.replace(
    'data-ru="июн 2023 \u2014 \u043f\u043e \u043d\u0430\u0441\u0442. \u0432\u0440\u0435\u043c\u044f" data-en="Jun 2023 \u2014 Present">\u0438\u044e\u043d 2023 \u2014 \u043f\u043e \u043d\u0430\u0441\u0442. \u0432\u0440\u0435\u043c\u044f',
    'data-ru="\u0438\u044e\u043d 2023 \u2014 \u043e\u043a\u0442 2026" data-en="Jun 2023 \u2014 Oct 2026">\u0438\u044e\u043d 2023 \u2014 \u043e\u043a\u0442 2026',
)
# plain dashes variant
t2 = t2.replace(
    'data-ru="июн 2023 — по наст. время" data-en="Jun 2023 — Present">июн 2023 — по наст. время',
    'data-ru="июн 2023 — окт 2026" data-en="Jun 2023 — Oct 2026">июн 2023 — окт 2026',
)
t2 = t2.replace(
    'data-ru="Crypto Industry International, ОАЭ" data-en="Crypto Industry International, UAE">Crypto Industry International, ОАЭ',
    'data-ru="NDA (ОАЭ, Дубай)" data-en="NDA (UAE, Dubai)">NDA (ОАЭ, Дубай)',
)
Path('index.html').write_text(t2, encoding='utf-8')
print('nda patched', 'NDA' in t2)

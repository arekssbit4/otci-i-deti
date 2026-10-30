# -*- coding: utf-8 -*-
"""Замена плейсхолдеров новых реплик рассказчика на настоящие хэши.

Схема та же, что в tools/check_voice.py: имя файла =
sha1("narrator|<текст>")[:16], текст - следующая реплика после play_narrator.
Вывод только ascii-маркерами (консоль cp1251).

Запуск из корня проекта: py tools/hash_new_narrator.py
"""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"

NARRATOR_RE = re.compile(r'^\$ play_narrator\("(0{10,}[0-9a-f]{0,6})"\)$')
SAY_RE = re.compile(r'^(?:[a-z_]+\s+)?"(.*)"$')


def file_hash(text):
    return hashlib.sha1(f"narrator|{text}".encode("utf-8")).hexdigest()[:16]


def main():
    lines = SCRIPT.read_text(encoding="utf-8").split("\n")
    changed = 0
    seen = {}
    for index, line in enumerate(lines):
        match = NARRATOR_RE.match(line.strip())
        if not match:
            continue
        placeholder = match.group(1)
        if len(placeholder) != 16 or set(placeholder) <= {"0"}:
            print("BAD_PLACEHOLDER_AT", index + 1, placeholder)
            return 1
        text = None
        for following in lines[index + 1:index + 5]:
            stripped = following.strip()
            if not stripped or stripped.startswith("#"):
                continue
            say = SAY_RE.match(stripped)
            text = say.group(1) if say else None
            break
        if text is None:
            print("NO_SAY_LINE_AT", index + 1)
            return 1
        if text in seen:
            print("DUPLICATE_TEXT_AT", index + 1, seen[text])
            return 1
        digest = file_hash(text)
        seen[text] = index + 1
        lines[index] = line.replace(match.group(1), digest)
        changed += 1
    SCRIPT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("HASHED", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Сверка озвучки с текстом сценария.

Имя файла реплики - это sha1("<персонаж>|<текст>")[:16]. Скрипт проверяет,
что каждый voice-файл соответствует своей реплике, и находит файлы, на
которые никто не ссылается.

У рассказчика два набора файлов (voice/narrator/ и voice/narrator_m/) с
одинаковыми именами, поэтому в сценарии стоят вызовы
$ play_narrator("<хэш>"), и проверяются сразу оба файла.

Запуск из корня проекта: py tools/check_voice.py
"""

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"
VOICE_DIR = ROOT / "game" / "voice"

VOICE_RE = re.compile(r'^voice "voice/([a-z_]+)/([0-9a-f]{16})\.mp3"$')
NARRATOR_RE = re.compile(r'^\$ play_narrator\("([0-9a-f]{16})"\)$')
SAY_RE = re.compile(r'^(?:[a-z_]+\s+)?"(.*)"$')

NARRATOR_FOLDERS = ("narrator", "narrator_m")


def file_hash(character, text):
    return hashlib.sha1(f"{character}|{text}".encode("utf-8")).hexdigest()[:16]


def find_say(lines, start):
    for line in lines[start:start + 4]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = SAY_RE.match(stripped)
        return match.group(1) if match else None
    return None


def main():
    lines = SCRIPT.read_text(encoding="utf-8").splitlines()
    errors = []
    references = {}
    statements = 0

    for index, line in enumerate(lines):
        stripped = line.strip()
        where = f"game/script.rpy:{index + 1}"

        narrator = NARRATOR_RE.match(stripped)
        if narrator:
            name = narrator.group(1)
            text = find_say(lines, index + 1)
            if text is None:
                errors.append(f"{where}: после play_narrator нет реплики")
                continue

            statements += 1
            for folder in NARRATOR_FOLDERS:
                references.setdefault(f"{folder}/{name}.mp3", []).append(index + 1)

            expected = file_hash("narrator", text)
            if name != expected:
                errors.append(
                    f"{where}: рассказчик ссылается на {name}.mp3, "
                    f"а текст даёт {expected}.mp3"
                )
            continue

        match = VOICE_RE.match(stripped)
        if not match:
            continue

        character, name = match.groups()
        text = find_say(lines, index + 1)

        if text is None:
            errors.append(f"{where}: после voice нет реплики")
            continue

        statements += 1
        references.setdefault(f"{character}/{name}.mp3", []).append(index + 1)

        expected = file_hash(character, text)
        if name != expected:
            errors.append(
                f"{where}: {character} ссылается на {name}.mp3, "
                f"а текст даёт {expected}.mp3"
            )

    for path in sorted(VOICE_DIR.rglob("*.mp3")):
        relative = path.relative_to(VOICE_DIR).as_posix()
        if relative not in references:
            errors.append(f"game/voice/{relative}: файл не используется")

    for relative in sorted(references):
        if not (VOICE_DIR / relative).exists():
            errors.append(f"game/voice/{relative}: файл отсутствует")

    print(f"voice-ссылок: {statements}, "
          f"файлов: {len(list(VOICE_DIR.rglob('*.mp3')))}")

    if errors:
        print(f"\nНайдено проблем: {len(errors)}")
        for error in errors:
            print("  " + error)
        return 1

    print("всё сходится")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Генерация озвучки рассказчика в оба набора: narrator/ (женский) и
narrator_m/ (мужской).

Имена файлов совпадают со схемой tools/check_voice.py:
sha1("narrator|<текст>")[:16]; тексты берутся прямо из game/script.rpy
(строки $ play_narrator("<хэш>") и следующая за ней реплика).
Существующие файлы пропускаются, досинтезируются только новые.

Запуск из корня проекта: py tools/tts_narrator_both.py
Нужен edge-tts (pip install edge-tts) и доступ в сеть.
"""

import asyncio
import re
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"
VOICE_DIR = ROOT / "game" / "voice"

NARRATOR_RE = re.compile(r'^\$ play_narrator\("([0-9a-f]{16})"\)$')
SAY_RE = re.compile(r'^(?:[a-z_]+\s+)?"(.*)"$')

# (папка, голос, скорость, тон) - как в README.md, таблица "Озвучка":
# рассказчик женский - Svetlana +5 % / -2 Гц, мужской - Dmitry +0 % / -2 Гц
SETS = (
    ("narrator", "ru-RU-SvetlanaNeural", "+5%", "-2Hz"),
    ("narrator_m", "ru-RU-DmitryNeural", "+0%", "-2Hz"),
)
CONCURRENCY = 4
ATTEMPTS = 12


def narrator_lines():
    lines = SCRIPT.read_text(encoding="utf-8").splitlines()
    found = {}
    for index, line in enumerate(lines):
        match = NARRATOR_RE.match(line.strip())
        if not match:
            continue
        for following in lines[index + 1:index + 5]:
            stripped = following.strip()
            if not stripped or stripped.startswith("#"):
                continue
            say = SAY_RE.match(stripped)
            if say:
                found[match.group(1)] = say.group(1)
            break
    return sorted(found.items())


async def synthesize(path, text, voice, rate, pitch, semaphore, failures):
    if path.exists() and path.stat().st_size > 0:
        return
    tmp = path.with_suffix(".part")
    async with semaphore:
        for attempt in range(1, ATTEMPTS + 1):
            try:
                await asyncio.wait_for(
                    edge_tts.Communicate(
                        text, voice, rate=rate, pitch=pitch, receive_timeout=30,
                    ).save(str(tmp)), timeout=60)
                tmp.replace(path)
                print(path.name, path.stat().st_size, "B", flush=True)
                return
            except Exception as error:
                if attempt == ATTEMPTS:
                    failures.append((str(path), repr(error)))
                    print(path.name, "FAILED", flush=True)
                else:
                    await asyncio.sleep(min(attempt, 3) * 0.4)


async def main():
    lines = narrator_lines()
    print("narrator_lines", len(lines))
    semaphore = asyncio.Semaphore(CONCURRENCY)
    failures = []
    for folder, voice, rate, pitch in SETS:
        out_dir = VOICE_DIR / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for stale in out_dir.glob("*.part"):
            stale.unlink()
        await asyncio.gather(*(
            synthesize(out_dir / f"{name}.mp3", text, voice, rate, pitch,
                       semaphore, failures)
            for name, text in lines
        ))
    print(f"done: {len(lines) * len(SETS) - len(failures)}"
          f" of {len(lines) * len(SETS)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

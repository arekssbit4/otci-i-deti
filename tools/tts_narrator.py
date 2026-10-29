"""Генерация озвучки рассказчика (мужской голос).

Женские файлы лежат в game/voice/narrator/, мужские - в
game/voice/narrator_m/ с теми же именами: sha1("narrator|<текст>")[:16].
Скрипт берёт тексты прямо из script.rpy и синтезирует только мужской набор,
поэтому имена остаются согласованными со сценарием.

Запуск из корня проекта: py tools/tts_narrator.py
Нужен edge-tts (pip install edge-tts) и доступ в сеть.
"""

import asyncio
import re
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"
OUT_DIR = ROOT / "game" / "voice" / "narrator_m"

VOICE_RE = re.compile(r'^voice "voice/narrator/([0-9a-f]{16})\.mp3"$')
NARRATOR_RE = re.compile(r'^\$ play_narrator\("([0-9a-f]{16})"\)$')
SAY_RE = re.compile(r'^(?:[a-z_]+\s+)?"(.*)"$')

VOICE = "ru-RU-DmitryNeural"
RATE = "+0%"
PITCH = "-2Hz"
CONCURRENCY = 2
ATTEMPTS = 30


def narrator_lines():
    lines = SCRIPT.read_text(encoding="utf-8").splitlines()
    found = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        match = NARRATOR_RE.match(stripped) or VOICE_RE.match(stripped)
        if not match:
            continue
        for following in lines[index + 1:index + 5]:
            stripped = following.strip()
            if not stripped or stripped.startswith("#"):
                continue
            say = SAY_RE.match(stripped)
            if say:
                found.append((match.group(1), say.group(1)))
            break
    return found


async def synthesize(name, text, semaphore, failures):
    path = OUT_DIR / f"{name}.mp3"
    if path.exists() and path.stat().st_size > 0:
        return
    tmp = OUT_DIR / f"{name}.part"
    async with semaphore:
        for attempt in range(1, ATTEMPTS + 1):
            try:
                await edge_tts.Communicate(
                    text, VOICE, rate=RATE, pitch=PITCH, receive_timeout=30,
                ).save(str(tmp))
                tmp.replace(path)
                print(f"{name}.mp3 ({path.stat().st_size} B)", flush=True)
                return
            except Exception as error:
                if attempt == ATTEMPTS:
                    failures.append((name, repr(error)))
                    print(f"{name}.mp3: не удалось - {error}", flush=True)
                else:
                    await asyncio.sleep(min(attempt, 3) * 0.4)


async def main():
    lines = narrator_lines()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUT_DIR.glob("*.part"):
        stale.unlink()
    semaphore = asyncio.Semaphore(CONCURRENCY)
    failures = []
    await asyncio.gather(*(synthesize(name, text, semaphore, failures) for name, text in lines))
    print(f"готово: {len(lines) - len(failures)} из {len(lines)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

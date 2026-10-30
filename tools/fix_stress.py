# -*- coding: utf-8 -*-
"""Пересинтез озвучки рассказчика с исправленными ударениями (задача 3).

Контекст (заказчик):
    TTS читает "мужчина лет сорока" как "сорокА" (птица), а надо "сОрока"
    (число 40). script.rpy НЕ трогаем: отображаемый текст, $ play_narrator
    ("<хэш>") и имена mp3 остаются эталонными. Меняем ТОЛЬКО текст, который
    подаём в синтез речи. Имена файлов = sha1("narrator|<текст из
    script.rpy>")[:16] - check_voice.py проверяет имена, не содержимое,
    поэтому пересинтез его не ломает.

Эмпирическая проверка способа (a) (October 2026, Temp/stress_test2/):
    1. Один и тот же текст дважды -> Байт-в-байт идентичный mp3
       (plain1 sha == plain2 sha): движок детерминирован, сравнение осмысленно.
    2. Текст с U+0301 после первой "о" ("сóрока") даёт ДРУГОЙ sha и
       отличается по размеру от варианта с марком после конечной "а"
       ("сорока́", птица): 14400 B против 14544 B, идентичный вход всегда
       даёт идентичный输出. Вывод: edge-tts (ru-RU Dmitry/Svetlana) НЕ
       игнорирует комбайнинг-марк - реагирует на него и на позицию.
    Значит способ (a) - основной; (b) контекстный перефраз и (c) фонетика
    не понадобились (запасные варианты задокументированы в таблице ниже).

Скан-лист (tools/scan_stress.py, дамп stress_scan_report.txt) составлен по
ФАКТИЧЕСКИМ словам всех 185 строк рассказчика. Исправляются только слова с
документированным словарным ударением, где движок систематически ошибается
(омографы, глаголы типа звонИт/звенЯт, редкие лексемы). Слова, где ударение
движком читается нормально ("сорок" в "вёрст на сорок" - числительное без
омографии, "клонится", "пристав", "корчма" - словарно ко́рчма, риск минимальный),
НЕ перезаписываем: правило заказчика - верные mp3 не трогать.

Запуск из корня проекта: py tools/fix_stress.py
Нужен edge-tts и сеть. Перезаписывает ТОЛЬКО перечисленные ключи, в оба набора:
    narrator/    = ru-RU-SvetlanaNeural +5% -2Hz   (женский, README.md)
    narrator_m/  = ru-RU-DmitryNeural   +0% -2Hz   (мужской, tts_narrator.py)
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

ACUTE = "\u0301"  # COMBINING ACUTE ACCENT; ставится СРАЗУ ПОСЛЕ гласной

SETS = (
    ("narrator", "ru-RU-SvetlanaNeural", "+5%", "-2Hz"),
    ("narrator_m", "ru-RU-DmitryNeural", "+0%", "-2Hz"),
)
ATTEMPTS = 30      # заказчик: при лимитах - 30 попыток, не сдаваться молча
CONCURRENCY = 2

# ---------------------------------------------------------------------------
# <16-хэш> = (слово_в_оригинале, слово_для_синтеза, обоснование)
# Оригинальный текст НЕ хранится в таблице - он берётся из script.rpy, а
# вокализуемый текст = оригинал с пословной заменой (гарантия, что кроме
# ударной гласной ничего не меняется; способ (b) перефразом не используется).
# ---------------------------------------------------------------------------
STRESS_FIXES = {
    # Подтверждённый заказчиком косяк (строка 168 script.rpy).
    # Способ (a): марк на первой "о" -> "сОрока" = число 40.
    # Запасной (b), не понадобился: "лет сорока" -> "лет сорок" для аудио.
    # Запасной (c), не понадобился: фонетика "сарока".
    "08996b264a128420": ("сорока", "со" + ACUTE + "рока",
                         "сОрока=40 vs сорокА=птица, омограф"),
    # "звенЯт" - та же ударная семья, что звонИт (движок склонен к "звЕнят").
    "50ffd86797fc5638": ("Звенят", "Звеня" + ACUTE + "т",
                         "звенЯт колокола, не звЕнят"),
    # Ушаков/Зализняк: щекота́ть -> 3sg "щекОчет" (корневое -о-).
    "81fe1a38afb84bb5": ("щекочет", "щек" + "о" + ACUTE + "чет",
                         "щекОчет, редкий глагол"),
    # Крылатое "ломотЬ" (второе "о"); встречается в новой ветке развязки сена.
    "8e9d9088df84b0da": ("ломоть", "ломо" + ACUTE + "ть",
                         "ломотЬ, ударение на второе о"),
    # "тарантАс" - старинный экипаж, конечное ударение.
    "e7582668031e6eea": ("Тарантас", "Таранта" + ACUTE + "с",
                         "тарантАс, редкое слово"),
    # "фаэто́н" - две подряд идущие строки с этим словом.
    "fbf264049611eb9f": ("фаэтон", "фаэто" + ACUTE + "н",
                         "фаэто́н, конечное ударение"),
    "0f8116f94738aae0": ("фаэтона", "фаэто" + ACUTE + "на",
                          "фаэто́на (род. падеж, ударение то же)"),
}


def narrator_lines():
    """Парсер как в check_voice.py: хэш + следующая реплика-текст."""
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
    return found


def build_jobs():
    texts = narrator_lines()
    jobs = []
    for key, (word, marked, why) in STRESS_FIXES.items():
        original = texts[key]
        if word not in original:
            raise SystemExit("STRESS FIX ABORT: %s word %r not in script text"
                             % (key, word))
        # единственная замена; проверяем, что слово встречается ровно один раз
        if original.count(word) != 1:
            raise SystemExit("STRESS FIX ABORT: %s word %r count %d != 1"
                             % (key, word, original.count(word)))
        synth = original.replace(word, marked)
        assert synth != original
        # марк обязан стоять сразу после гласной - проверка attach
        pos = synth.index(ACUTE)
        prev = synth[pos - 1]
        assert prev in "аеёиоуыэюяАЕЁИОУЫЭЮЯ", (key, repr(synth[pos-2:pos+1]))
        jobs.append((key, original, synth, why))
        print("PLAN", key, "word", ascii(word), "->", ascii(marked))
    return jobs


async def synthesize(path, text, voice, rate, pitch, semaphore):
    """Принудительная перезапись (в отличие от tts_narrator_both.skip)."""
    tmp = path.with_suffix(".part")
    async with semaphore:
        for attempt in range(1, ATTEMPTS + 1):
            try:
                await asyncio.wait_for(
                    edge_tts.Communicate(
                        text, voice, rate=rate, pitch=pitch,
                        receive_timeout=30).save(str(tmp)), timeout=60)
                tmp.replace(path)
                print("OK", path.parent.name, path.name,
                      path.stat().st_size, "B", flush=True)
                return True
            except Exception as error:
                if attempt == ATTEMPTS:
                    print("FAILED", path.parent.name, path.name,
                          repr(error)[:90], flush=True)
                    return False
                await asyncio.sleep(min(attempt, 3) * 0.5)
    return False


async def main():
    jobs = build_jobs()
    semaphore = asyncio.Semaphore(CONCURRENCY)
    tasks = []
    for folder, voice, rate, pitch in SETS:
        out_dir = VOICE_DIR / folder
        for stale in out_dir.glob("*.part"):
            stale.unlink()
        for key, original, synth, why in jobs:
            tasks.append(synthesize(out_dir / (key + ".mp3"), synth,
                                    voice, rate, pitch, semaphore))
    results = await asyncio.gather(*tasks)
    done = sum(1 for r in results if r)
    print("done", done, "of", len(results))
    return 0 if done == len(results) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

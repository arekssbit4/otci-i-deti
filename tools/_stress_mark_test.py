# -*- coding: utf-8 -*-
"""Эмпирическая проверка: игнорирует ли edge-tts (ru-RU) комбайнинг-марк
U+0301 или нет, и детерминирован ли вывод вообще.

Тестовые короткие фразы синтезируются в Temp/stress_test/. Сравнение по
байтам и по размеру (длительности): два одинаковых текста дают базу
детерминизма; текст с марком и с марком на другой гласной - реагирует ли
движок и по-разному ли на разные позиции ударения.

Запуск: py tools/_stress_mark_test.py
"""

import asyncio
import hashlib
from pathlib import Path

import edge_tts

OUT = Path("C:/Users/AReKS/AppData/Local/Temp/stress_test")
VOICE = "ru-RU-DmitryNeural"
RATE, PITCH = "+0%", "-2Hz"

ACUTE = "\u0301"

SAMPLES = {
    # control: same text twice -> determinism check
    "plain_a1": "мужчина лет сорока с небольшим",
    "plain_a2": "мужчина лет сорока с небольшим",
    # mark on first O (correct: number 40)
    "mark_so": "мужчина лет с" + ACUTE + "рока с небольшим",
    # mark on final A (bird reading)
    "mark_sa": "мужчина лет сорок" + ACUTE + " с небольшим",
    # paraphrase variant (method b)
    "para": "мужчина лет сорок с небольшим",
    # single-word minimal pair
    "word_plain": "сорока",
    "word_mark1": "с" + ACUTE + "рока",
    "word_mark2": "сорок" + ACUTE + "а",
}


async def one(name, text):
    data = bytearray()
    comm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH,
                               receive_timeout=30)
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            data.extend(chunk["data"])
    path = OUT / (name + ".mp3")
    path.write_bytes(bytes(data))
    return name, len(data), hashlib.sha256(bytes(data)).hexdigest()[:12]


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    for name, text in SAMPLES.items():
        # retry: endpoint flakiness
        for attempt in range(8):
            try:
                n, size, digest = await asyncio.wait_for(one(name, text), 60)
                res[n] = (size, digest)
                break
            except Exception as e:
                if attempt == 7:
                    print(name, "FAILED", repr(e)[:80])
                else:
                    await asyncio.sleep(0.5)
    for name in SAMPLES:
        if name in res:
            print("%-12s size=%7d sha=%s" % (name, res[name][0], res[name][1]))
    if "plain_a1" in res and "plain_a2" in res:
        print("determinism_identical:", res["plain_a1"] == res["plain_a2"])
    if "plain_a1" in res and "mark_so" in res:
        print("mark_changes_output:", res["plain_a1"] != res["mark_so"])
    if "mark_so" in res and "mark_sa" in res:
        print("mark_position_matters:", res["mark_so"] != res["mark_sa"])
    return 0


if __name__ == "__main__":
    asyncio.run(main())

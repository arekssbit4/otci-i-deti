## Голос рассказчика ##########################################################
##
## Реплики рассказчика озвучены двумя голосами. Файлы лежат в
## game/voice/narrator/ (женский) и game/voice/narrator_m/ (мужской) под
## одними и теми же именами, поэтому сценарий хранит только хэш реплики,
## а папку выбирает play_narrator().

default persistent.narrator_gender = "f"

init python:

    NARRATOR_FOLDERS = {
        "f": "narrator",
        "m": "narrator_m",
    }

    def play_narrator(key):
        folder = NARRATOR_FOLDERS.get(persistent.narrator_gender, "narrator")
        voice("voice/%s/%s.mp3" % (folder, key))

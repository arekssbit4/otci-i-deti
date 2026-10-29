# ============================================================
# РАЗВЯЗКИ И СЦЕНЫ
# ============================================================

init python:

    ENDINGS = [
        ("дом", "Живая жизнь",
         "Аркадий и Катя остаются в Марьине. Трое детей, переводы Николая Петровича, "
         "Фенечка, которая держит весь дом.", "bg/maryino_terrace.png"),
        ("одна", "Невозвратное",
         "Анна Сергеевна приезжает на кладбище одна, без слуг, "
         "и не говорит старикам, кто она.", "bg/cemetery.png"),
        ("один", "Один в поле",
         "Тот же постоялый двор десятью годами позже - и привычка говорить вслух "
         "с тем, кого больше нет.", "bg/theInnBG.jpeg"),
    ]

    SCENES = [
        ("scene_1", "Глава I–II", "Постоялый двор"),
        ("scene_2", "Глава III–IV", "Марьино. Вечер"),
        ("scene_2b", "Глава V", "История одного брата"),
        ("scene_3", "Глава VI–VIII", "Утро в Марьине"),
        ("scene_4", "Глава IX–XVII", "Молодые люди · Бал · Никольское"),
        ("scene_5", "Глава XVIII–XIX", "Ночь перед рассветом"),
        ("scene_5b", "Глава XXV–XXVI", "Васильевка"),
        ("scene_6", "Глава XXVII", "Скорбный тиф"),
        ("scene_7", "Эпилог · 1", "Свадьбы"),
        ("scene_8", "Эпилог · 2", "Могила"),
    ]

    def unlock_ending(key):
        if key not in persistent.endings:
            persistent.endings = list(persistent.endings) + [key]
            renpy.save_persistent()
            return True
        return False

    def unlock_scene(key):
        if key not in persistent.scenes_seen:
            persistent.scenes_seen = list(persistent.scenes_seen) + [key]
            renpy.save_persistent()


default persistent.endings = []
default persistent.scenes_seen = ["scene_1"]


screen endings():

    tag menu

    $ opened = len(persistent.endings or [])

    use game_menu(_("Развязки"), scroll="viewport", spacing=20):

        vbox:
            spacing 18

            text _("Открыто [opened] из 3"):
                style "extras_counter"

            for key, title, description, thumb in ENDINGS:
                $ known = key in (persistent.endings or [])

                frame:
                    style "extras_card"

                    hbox:
                        spacing 30

                        if known:
                            add thumb xysize (340, 191)
                        else:
                            frame:
                                style "extras_thumb_locked"
                                text _("?") style "extras_thumb_question"

                        vbox:
                            xfill True
                            spacing 10

                            if known:
                                text title style "extras_title"
                                text description style "extras_description"
                            else:
                                text _("Развязка не открыта") style "extras_title"
                                text _("Дойдите до финала по другой дороге - и она откроется."):
                                    style "extras_description"


screen scenes():

    tag menu

    $ opened = len(persistent.scenes_seen or [])

    use game_menu(_("Сцены"), scroll="viewport", spacing=12):

        vbox:
            spacing 8

            text _("Открыто [opened] из 10") style "extras_counter"
            text _("Сцену можно начать заново в любой момент - выбор в ней будет считаться с чистого листа."):
                style "extras_description"
            null height 12

            for label_name, chapter, place in SCENES:
                $ known = label_name in (persistent.scenes_seen or [])
                $ caption = "%s · %s" % (chapter, place if known else "???")

                textbutton caption:
                    action Start(label_name)
                    sensitive known
                    style "scene_button"


style extras_counter is gui_text:
    color gui.accent_color
    size 28

style extras_card is frame:
    xfill True
    padding (40, 22)

style extras_title is gui_text:
    size 40
    color gui.accent_color

style extras_description is gui_text:
    size 28
    color "#d8d8d8"

style extras_thumb_locked is frame:
    xsize 340
    ysize 191
    background "#0f1622"
    padding (0, 0)

style extras_thumb_question is gui_text:
    size 84
    color "#3d4c63"
    xalign 0.5
    yalign 0.5

style scene_button is choice_button:
    xsize 1180

style scene_button_text is button_text:
    size 30
    xsize 880
    xalign 0.0


## Титры ######################################################################

screen credits():

    zorder 200

    add Solid("#0b0f16")

    key "game_menu" action MainMenu(confirm=False)

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20

        text _("ОТЦЫ И ДЕТИ") style "credits_title"
        text _("по роману И. С. Тургенева") style "credits_subtitle"

        null height 28

        text _("Идея и разработка · @wherearethechoice · @arekssbit4") style "credits_text"
        text _("Сценарий, графика и озвучка · CC BY-NC-SA 4.0") style "credits_text"
        text _("Код .rpy · MIT") style "credits_text"
        text _("Движок Ren'Py 8.5 · шрифт PT Serif, SIL OFL 1.1") style "credits_text"

        null height 36

        hbox:
            xalign 0.5
            spacing 64

            textbutton _("В главное меню") action MainMenu(confirm=False)

            textbutton _("Пройти заново") action Start()


style credits_title is gui_text:
    size 64
    color gui.accent_color
    xalign 0.5

style credits_subtitle is gui_text:
    size 30
    color "#cfd8e3"
    xalign 0.5

style credits_text is gui_text:
    size 26
    color "#9fb0c8"
    xalign 0.5

init python:
    renpy.music.register_channel("bgs", "sfx", loop=True)

# ============================================================
# ПЕРСОНАЖИ
# ============================================================
## Имена говорящих читаются с пергаментного namebox (#dbcfb4), поэтому цвета -
## тёмные чернила, а не пастель: пастель на светлой бумаге давала контраст
## 1.2:1. Оттенки подобраны по прежнему «семейству» персонажа и все держат
## контраст >= 4.5:1 (WCAG AA).
define arcardy = Character('Аркадий', color="#2f5d33")
define bazarov = Character('Базаров', color="#1f3a63")
define nikolay = Character('Николай Петрович', color="#7a4a12")
define pavel = Character('Павел Петрович', color="#5a2f6e")
define anna = Character('Анна Сергеевна', color="#8c2438")
define fedosiya = Character('Фенечка', color="#8a3a17")
define mitya = Character('Митя', color="#6b5310")
define catya = Character('Катя', color="#93326e")
define vasiliy = Character('Василий Иванович', color="#2a5a52")
define arina = Character('Арина Власьевна', color="#6e2417")
define petr = Character('Пётр')
define prokofiy = Character('Прокофьич')
define dunyasha = Character('Дуняша')

# Голоса без спрайтов — второстепенные лица романа
define smit = Character('Ситников', color="#1f5c7a")
define kozy = Character('Козьин', color="#33525a")
define liza = Character('Лиза', color="#6e2a5a")
define foma = Character('Фома', color="#4f5220")
define doct = Character('Доктор', color="#3a4463")

# ============================================================
# Фоны
# ============================================================
image theInn = "bg/theInnBG.jpeg"
image maryino_terrace = "bg/maryino_terrace.png"
image maryino_morning = "bg/maryino_morning.png"
image maryino_room = "bg/maryino_room.png"
image ball = "bg/ball.png"
image nikolskoe = "bg/nikolskoe.png"
image garden_duel = "bg/garden_duel.png"
image bazarov_room = "bg/bazarov_room.png"
image church_wedding = "bg/church_wedding.png"
image cemetery = "bg/cemetery.png"

# ============================================================
# Спрайты
# ============================================================
image arcardiydef = "arcadiy/arcadiydefault.png"
image bazarovdef = "bazarov/bazarovdefault.png"
image nikolaydef = "nikolay/nikolaydefault.png"
image paveldef = "pavel/paveldefault.png"
image annadef = "anna/annadefault.png"
image fedosiyadef = "fedosiya/fedosiyadefault.png"
image catyadef = "catya/catyadefault.png"
image vasiliydef = "vasiliy/vasiliydefault.png"
image arinadef = "arina/arinadefault.png"
image petrdef = "petr/petrdefault.png"

# ============================================================
# РАСПОЛОЖЕНИЕ
# ============================================================
transform left_char:
    xalign -0.02
    yalign 1.0
    zoom 0.84

transform right_char:
    xalign 1.02
    yalign 1.0
    zoom 0.84

transform center_char:
    xalign 0.5
    yalign 1.0
    zoom 0.86

# третий собеседник — дальше, меньше, в стороне
transform side_char:
    xalign 0.33
    yalign 1.0
    zoom 0.60
    alpha 0.92

transform side_right_char:
    xalign 0.67
    yalign 1.0
    zoom 0.60
    alpha 0.92

# призрачные планы: воспоминание, бред, память
transform left_ghost:
    xalign -0.02
    yalign 1.0
    zoom 0.84
    alpha 0.55

transform right_ghost:
    xalign 1.02
    yalign 1.0
    zoom 0.84
    alpha 0.55

transform center_ghost:
    xalign 0.5
    yalign 1.0
    zoom 0.86
    alpha 0.50

transform bg_kb:
    on show:
        zoom 1.0
        linear 40.0 zoom 1.06

transform bg_kb_slow:
    on show:
        zoom 1.07
        linear 55.0 zoom 1.0

# ============================================================
# ПЕРЕМЕННЫЕ ПРОХОЖДЕНИЯ
# ============================================================
default kinship = 0            # тяга Аркадия к дому, отцу, земле
default nihil = 0              # тяга Аркадия к Базарову и к разрыву с прошлым
default anna_open = 0          # линия Одинцовой: её отклик и его смелость
default mercy = 0              # участие, верность, смилостивление
default pavel_history = False  # Аркадий знает историю княгини Н.
default saw_last_hours = False # был у постели до конца
default duel_warned = False    # попытался предотвратить дуэль
default bazarov_spoke_all = False  # выговорился Одинцовой до конца
default cold_hello = False     # сдержанная встреча с отцом в 1-й главе
default ending = ""            # имя развязки
default speta_branch = False   # ветка X: вслух заступиться за Пушкина
default hay_branch = False     # ветка XXI: договорить слово о сене
default katya_branch = False   # ветка XXV: не сказать Кате в саду

# ============================================================
# СЛУЖЕБНЫЕ МЕТКИ
# ============================================================
label chapter_card(chapter_text, subtitle_text):
    scene black
    with fade
    centered "{size=46}{b}[chapter_text]{/b}{/size}\n\n{size=32}[subtitle_text]{/size}"
    return


label start:

    scene black
    with fade

    centered "{size=74}{b}ОТЦЫ И ДЕТИ{/b}{/size}\n\n{size=30}по роману И. С. Тургенева{/size}\n\n{size=22}игра с выбором · шесть развязок{/size}"

    jump scene_1


# ============================================================
# СЦЕНА 1. Постоялый двор (главы I–II)
# ============================================================
label scene_1:

    call chapter_card("ГЛАВА I–II", "Постоялый двор") from _card1

    scene theInn at bg_kb
    with fade

    play music "music/waiting_theme.ogg" fadein 1.0 volume 0.9
    play bgs "music/light-breeze.ogg" volume 0.4

    $ play_narrator("7de18f9e53aaf682")
    "Май 1859 года. Солнце уже клонится к закату, но всё ещё жжёт пыльную большую дорогу."
    $ play_narrator("08996b264a128420")
    "На низком крылечке захудалого постоялого двора стоит мужчина лет сорока с небольшим — Николай Петрович Кирсанов."
    $ play_narrator("2816618f278a6e34")
    "Запылённое пальто, клетчатые панталоны, усталый взгляд. Ветерок доносит запах тёплого ржаного хлеба из сеней."
    $ play_narrator("d24017af600cd4e2")
    "Где-то вдалеке слышится стук колёс. Николай Петрович нервно смотрит вдоль дороги."

    show nikolaydef at center_char
    with dissolve

    voice "voice/nikolay/eb41d6ebaca0d6e4.mp3"
    nikolay "Что, Пётр, не видать ещё?"

    hide nikolaydef
    show petrdef at center_char
    with dissolve

    voice "voice/petr/0687a5e60199ca6b.mp3"
    petr "Никак нет-с, не видать."

    hide nikolaydef
    show nikolaydef at center_char
    with dissolve

    voice "voice/nikolay/55f2de2c1d551c47.mp3"
    nikolay "Не видать?"

    hide nikolaydef
    show petrdef at center_char
    with dissolve

    voice "voice/petr/7670a124956305bf.mp3"
    petr "Не видать."

    $ play_narrator("b788d2b64936bcbf")
    "Проходит ещё верста; лошадь идёт шагом, и каждая минута вытягивается в верёвку."

    hide petrdef
    show nikolaydef at center_char
    with dissolve

    "{i}(тяжело вздыхает, садится, смотрит вдаль){/i}"
    voice "voice/nikolay/e8256af20434e116.mp3"
    nikolay "Сын… кандидат… Аркаша… Неужели уже совсем взрослый? Десять лет прошло как сон…"
    voice "voice/nikolay/32de4d249e3243b3.mp3"
    nikolay "А ведь я его таким маленьким помню, когда он ещё на руках у Маши сидел…"
    voice "voice/nikolay/3c885eb11c0add43.mp3"
    nikolay "{i}(тихо){/i} Не дождалась она…"

    hide nikolaydef
    show petrdef at center_char
    with dissolve

    "{i}(выныривает из-под ворот){/i}"
    voice "voice/petr/189dcb254cfbe437.mp3"
    petr "Никак они едут-с!"

    hide petrdef

    $ play_narrator("e7582668031e6eea")
    "Тарантас подъезжает. Аркадий выпрыгивает. Пыль не успела улететь, а Николай Петрович уже идёт к нему."

    show arcardiydef at right_char
    with dissolve

    voice "voice/arcardy/d887fb54253e5a70.mp3"
    arcardy "Дай же отряхнуться, папаша! Я тебя всего запачкаю."

    show nikolaydef at left_char
    with dissolve

    $ play_narrator("3c1da03b12b74b3d")
    "Аркадий оглядывает отца — и в горле у него что-то сжимается. Он не видел этого человека десять лет."

    menu:
        "Броситься к нему, обнять — как бросился бы десятилетним":
            $ kinship += 2
            "{i}(он сам не ждал от себя такой скорости){/i}"
            voice "voice/nikolay/fc59e024d7ed2bd3.mp3"
            nikolay "Ничего, ничего… Аркаша! Аркаша! Покажи-ка себя…"
            "{i}(обнимает крепко, со слезами, отодвигается, смотрит){/i}"
            voice "voice/nikolay/90fc7975317e5f82.mp3"
            nikolay "Какой ты стал! Совсем взрослый… кандидат! Я уже и не знал, что думать."
            voice "voice/arcardy/26775874741cc3ff.mp3"
            arcardy "{i}(смеётся звонко){/i} Папаша, ты меня ждал часов пять, да? Добрый папаша!"

        "Подать руку и поклониться по-европейски, как договорился с собой в вагоне":
            $ cold_hello = True
            $ nihil += 1
            "{i}(он помнит, как кланяются в Петербурге, и делает всё чинно){/i}"
            voice "voice/nikolay/d6ce082aa7ca2cfa.mp3"
            nikolay "{i}(замирает на полувдохе, жмёт руку, потом всё-таки притягивает сына к себе){/i} Аркаша… Ну, полно церемоний. Покажи-ка себя."
            voice "voice/arcardy/20c9b1d93f9c293e.mp3"
            arcardy "Папаша, ты меня ждал часов пять, да?"
            voice "voice/nikolay/0cbc091c40977404.mp3"
            nikolay "{i}(смущённо){/i} Да часов около пяти… Я уже начал волноваться."
            $ play_narrator("310aeb94bf3777f9")
            "Николай Петрович отводит глаза, и что-то в его лице на миг становится старым."

        "Обнять быстро, почти небрежно — и тут же поймать себя на этом":
            $ kinship += 1
            $ mercy += 1
            "{i}(он обнимает коротко и виновато смотрит на отца){/i}"
            voice "voice/nikolay/d5a041c61bb67693.mp3"
            nikolay "Ничего, ничего… Я знаю, тебе неловко. Я понимаю. Ты городской стал."
            voice "voice/arcardy/c8fc203c29b3e2ee.mp3"
            arcardy "Нет, папаша. Мне не неловко. Мне страшно радостно, только я не умею…"
            voice "voice/nikolay/8b427e674f54c993.mp3"
            nikolay "{i}(глотает){/i} Умеешь. Ещё как умеешь."

    show nikolaydef at left_char
    show arcardiydef at right_char
    with dissolve

    voice "voice/nikolay/3776d66b3d00fc36.mp3"
    nikolay "А дядя твой Павел хотел со мной выехать навстречу, но почему-то раздумал в последний момент."

    voice "voice/arcardy/40df52ef33ca4aee.mp3"
    arcardy "Всё тот же Павел Петрович!"

    voice "voice/nikolay/ae7b1af7e6a335f1.mp3"
    nikolay "Он тебя ждёт… Он тебя очень ждёт, хотя и не скажет."

    "{i}(Аркадий целует отца в щёку.){/i}"

    if cold_hello:
        voice "voice/arcardy/ca7a9fc0309cfb17.mp3"
        arcardy "Папаша, позволь познакомить тебя с моим приятелем, Базаровым. О нём я тебе так часто писал."
    else:
        voice "voice/arcardy/6d527c007484406f.mp3"
        arcardy "Папаша, позволь познакомить тебя с моим добрым приятелем, Базаровым."
        voice "voice/arcardy/3c3d07438b43fe93.mp3"
        arcardy "О котором я тебе так часто писал. Он так любезен, что согласился погостить у нас."

    hide nikolaydef
    hide arcardiydef
    show bazarovdef at center_char
    with dissolve

    "{i}(Николай Петрович быстро оборачивается к Базарову, крепко жмёт ему руку){/i}"
    voice "voice/nikolay/26e90144e9eb86ea.mp3"
    nikolay "Душевно рад… и благодарен за доброе намерение посетить нас."
    voice "voice/nikolay/2b743fa81efd2895.mp3"
    nikolay "Позвольте узнать ваше имя и отчество?"

    voice "voice/bazarov/a9d2e18491316121.mp3"
    bazarov "{i}(лениво, мужественным голосом){/i} Евгений Васильев."

    voice "voice/nikolay/803f50f741ec7d36.mp3"
    nikolay "Надеюсь, любезнейший Евгений Васильич, что вы не соскучитесь у нас. У нас тихо, но воздух хороший, природа…"

    "{i}(Базаров чуть трогает губы улыбкой и приподнимает фуражку.){/i}"

    hide bazarovdef
    show arcardiydef at center_char
    with dissolve

    "{i}(отцу, тихо){/i}"
    voice "voice/arcardy/d329b0d42b5738e6.mp3"
    arcardy "Ты с ним, пожалуйста, не церемонься. Он чудесный малый, такой простой — ты увидишь."

    menu:
        "«Он мне очень нравится», — сказать отцу честно":
            $ kinship += 1
            voice "voice/arcardy/edd91cb25d4c1571.mp3"
            arcardy "И вообще… он мне очень нравится, папаша. Ты полюбишь его."
            voice "voice/nikolay/312ffc9cc99d9412.mp3"
            nikolay "{i}(кивает, но в глазах у него тень){/i} Если он тебе друг — и мне будет друг."
        "Промолчать и сесть в тарантас":
            $ nihil += 1
            "{i}(Аркадий садится в тарантас первым, не дожидаясь ответа.){/i}"
            $ play_narrator("99a04ed1300e28a8")
            "Николай Петрович ещё раз смотрит на дорогу, точно с чем-то прощается, и только тогда садится рядом."

    $ play_narrator("25bb8bf1f688ebf7")
    "Оба экипажа катят в Марьино. Аркадий радостно болтает всю дорогу — и всё-таки оглядывается на отца: тот молчит и смотрит в поле."

    stop bgs fadeout 1.5
    stop music fadeout 1.5

    jump scene_2


# ============================================================
# СЦЕНА 2. Марьино — ужин с Павлом Петровичем (главы III–IV)
# ============================================================
label scene_2:

    call chapter_card("ГЛАВА III–IV", "Марьино. Вечер") from _card2

    scene maryino_terrace at bg_kb
    with fade

    play music "music/light-breeze.ogg" fadein 1.5 volume 0.6

    $ play_narrator("5e2b3df650340cb9")
    "Усадьба Марьино. Новый деревянный дом с красной железной крышей. Вечер."
    $ play_narrator("364908ba2b8fc9d0")
    "На террасе накрыт ужин, пахнет сиренью и свежим сеном. Павел Петрович в идеальном английском костюме медленно прохаживается."

    show paveldef at right_char
    with dissolve
    show nikolaydef at left_char
    with dissolve

    "{i}(входя в гостиную){/i}"
    voice "voice/pavel/0b1bf1ccf25eefce.mp3"
    pavel "Кто сей?"

    voice "voice/nikolay/5f0edf14fe7e9c40.mp3"
    nikolay "Приятель Аркаши, очень, по его словам, умный человек."

    voice "voice/pavel/2e6b9eaec5792102.mp3"
    pavel "Он у нас гостить будет?"

    voice "voice/nikolay/b1fd8df5f73f1048.mp3"
    nikolay "Да."

    voice "voice/pavel/4c30d131665fa164.mp3"
    pavel "Этот волосатый?"

    "{i}(низкий поклон, вежливый и холодный){/i}"

    $ play_narrator("c42f221ab4a57b4d")
    "Базаров только что вернулся с болота — грязные сапоги, в руке мешок с лягушками. Атмосфера напряжённая, но пока вежливая."

    hide paveldef
    hide nikolaydef
    show bazarovdef at left_char
    with dissolve
    show paveldef at right_char
    with dissolve

    $ play_narrator("18673f8d08bd53ef")
    "За ужином разговор затягивается."

    voice "voice/pavel/a98e12c7e69a2bf7.mp3"
    pavel "{i}(медленно намазывая масло){/i} Вы столь высокого мнения о немцах?"

    voice "voice/bazarov/0a11f38d709c9aa0.mp3"
    bazarov "Тамошние учёные — дельный народ."

    voice "voice/pavel/56bc3ca13992e10d.mp3"
    pavel "А об русских учёных вы, вероятно, не имеете столь лестного понятия?"

    voice "voice/bazarov/0787e91d5b9a0bcc.mp3"
    bazarov "Пожалуй, что так."

    voice "voice/pavel/ec1722a146bae0d8.mp3"
    pavel "Это очень похвальное самоотвержение. Но как же нам Аркадий Николаич сейчас сказывал, что вы не признаёте никаких авторитетов? Не верите им?"

    voice "voice/bazarov/1d63410739bee21c.mp3"
    bazarov "Да зачем же я стану их признавать? И чему я буду верить? Мне скажут дело — я соглашаюсь, вот и всё."

    voice "voice/pavel/fbc85dc01155e741.mp3"
    pavel "А немцы все дело говорят?"

    voice "voice/bazarov/665182b807884d5c.mp3"
    bazarov "Не все."

    voice "voice/pavel/781d9172c42204ce.mp3"
    pavel "{i}(с иронией){/i} Что касается до меня, грешный человек, я немцев не жалую. О русских немцах я уже не упоминаю… Но и немецкие немцы мне не по нутру. Ещё прежние — Шиллер, Гёте… А теперь пошли всё какие-то химики да материалисты…"

    voice "voice/bazarov/77c9a506cadb5269.mp3"
    bazarov "{i}(резко перебивая){/i} Порядочный химик в двадцать раз полезнее всякого поэта."

    voice "voice/pavel/fffb890582487b79.mp3"
    pavel "{i}(приподнимая брови){/i} Вот как… Вы, стало быть, искусства не признаёте?"

    voice "voice/bazarov/93cfa6d1ff430f63.mp3"
    bazarov "{i}(с презрительной усмешкой){/i} Искусство наживать деньги, или нет более геморроя!"

    voice "voice/pavel/7b13896f32802325.mp3"
    pavel "Так-с… Значит, вы верите в одну науку?"

    voice "voice/bazarov/e9a8d7326afa6a60.mp3"
    bazarov "Я уже доложил вам, что ни во что не верю. И что такое наука — наука вообще? Есть науки, как есть ремесла, а наука вообще не существует вовсе."

    voice "voice/pavel/fd353aee2bac11d1.mp3"
    pavel "{i}(откладывает нож, уже без иронии){/i} Ничего не уважать… Вы это по-французски выговариваете изящно. А порядок, семья, религия — и это всё ничего?"

    voice "voice/bazarov/fdea2e27dcac7159.mp3"
    bazarov "Разрушение — прежде всего. Умные люди должны только разрушать. Дальше не всем дойдёт."

    voice "voice/pavel/20b63d8ee177528e.mp3"
    pavel "Дальше — хаос."

    voice "voice/bazarov/9ea510af734fae23.mp3"
    bazarov "А может, и дорога. Дороги-то, Павел Петрович, и нет. Так что и хаос вам не грозит: вы его доживёте в своём кабинете, с воротничком из камня."

    "{i}(Павел Петрович белеет. Николай Петрович тянется к колокольчику, чтобы остановить. Аркадий сидит, не поднимая глаз.){/i}"

    menu:
        "Вступиться за дядю: «Евгений, полно. Это мой отец и мой дядя»":
            $ kinship += 2
            voice "voice/arcardy/0b2c412b8bd5d814.mp3"
            arcardy "{i}(тихо, но твёрдо){/i} Евгений… Полно. Это мой дядя. И мой отец, который ради тебя снял с себя всё, что имел."
            voice "voice/bazarov/49f0ed46e9457c49.mp3"
            bazarov "{i}(усмешка гаснет){/i} Твой дядя сам начал. Я только докончил."
            voice "voice/pavel/b44ba953172da443.mp3"
            pavel "{i}(встаёт, кланяется брату и племяннику, не глядя на Базарова){/i} Я удаляюсь, чтобы не быть тебе стеснением, Николай. Ты видишь, он меня изучил."
            voice "voice/nikolay/9f883a96d9998796.mp3"
            nikolay "Павел… Ну, полно, брат…"
            voice "voice/pavel/42b642f230ea740c.mp3"
            pavel "Довольно. Я по горло нагрузился учтивостью."
            $ play_narrator("5fc43390519ba6d3")
            "Ужин кончается втягчивой тишиной. Но Базаров больше не скажет ни слова — и это тоже победа Аркадия."

        "Поддержать Базарова: «Не мешайте ему, дядюшка»":
            $ nihil += 2
            show arcardiydef at side_char
            with dissolve
            voice "voice/arcardy/257564592cd137e3.mp3"
            arcardy "{i}(с улыбкой){/i} Не мешайте ему, дядюшка. Он иначе просто не умеет. Он зол, только когда его перебивают."
            voice "voice/bazarov/cf6e6f2e98efb4a4.mp3"
            bazarov "{i}(одобрительно хмыкает){/i} Вот это по-нашему. Аркадий начинает понимать."
            voice "voice/pavel/08767378a333e80f.mp3"
            pavel "{i}(медленно поднимается, складывает салфетку){/i} Поздравляю, братец. Твой сын находит вкус в… мясничанье. Я к вашим услугам более не стояльщик."
            voice "voice/nikolay/adc74e251db6a0ae.mp3"
            nikolay "{i}(бледнея){/i} Павел!.. Аркадий!.. Да что вы, в самом деле…"
            "{i}(Дверь за Павлом Петровичем закрывается аккуратно, почти без звука. От этого звука Аркадию делается не по себе.){/i}"
            voice "voice/arcardy/9b1e5d0bc72f87df.mp3"
            arcardy "{i}(про себя){/i} Что-то я сказал лишнее."
            hide arcardiydef

        "Переменить разговор на хозяйство, на всё, что угодно":
            $ mercy += 1
            show arcardiydef at side_char
            with dissolve
            show nikolaydef at side_right_char
            with dissolve
            voice "voice/arcardy/8c897d954f1cf1e0.mp3"
            arcardy "{i}(быстро){/i} Папаша, а правда, что у тебя в этом году пшеница вышла лучше, чем в прошлом? Я Базарову говорил — он не поверил."
            voice "voice/nikolay/1948b7caf6791f99.mp3"
            nikolay "{i}(схватывается за соломинку){/i} Вестимо лучше! Мы, брат, с мёдом… то есть нет, мёд плох, а пшеница… Павел, ты слышишь, Аркаша про хозяйство спрашивает!"
            voice "voice/pavel/e0a262368d5e528d.mp3"
            pavel "{i}(сдержанно){/i} Слышу, братец. Хозяйство — дело положительное. Здесь хоть никто не разрушает."
            voice "voice/bazarov/097888ada7e821a8.mp3"
            bazarov "{i}(в сторону, Аркадию, вполголоса){/i} Ну, ты и дипломат. Тебя в министры, а нас — в лакеи."
            $ play_narrator("807a070b212e0814")
            "Ужин доходит до конца. Никто не победил, но и не разбили фарфор."
            hide arcardiydef
            hide nikolaydef

    hide paveldef
    hide bazarovdef
    hide arcardiydef
    hide nikolaydef
    with dissolve

    scene maryino_room at bg_kb
    with fade

    play music "music/waiting_theme.ogg" fadein 1.0 volume 0.4

    $ play_narrator("e673822068163422")
    "Ночью, в комнате Аркадия. Свеча догорает."

    show bazarovdef at left_char
    with dissolve
    show arcardiydef at right_char
    with dissolve

    voice "voice/bazarov/02a61f1f390fad74.mp3"
    bazarov "{i}(курит трубку, сидя на кровати){/i} Чудаковат у тебя дядя… Щегольство какое в деревне, подумаешь! Ногти-то, ногти, хоть на выставку посылай! Подбородок выбрит идеально."

    voice "voice/arcardy/0cf873b2245f2b52.mp3"
    arcardy "Да ведь ты не знаешь… Он львом был в своё время. Красавцем был, голову кружил женщинам. Я когда-нибудь расскажу тебе его историю."

    voice "voice/bazarov/7ef3d4606a2ea5ca.mp3"
    bazarov "По старой, значит, памяти. Пленять-то здесь, жаль, некого. Я всё смотрел — такие у него удивительные воротнички, точно каменные."

    voice "voice/arcardy/ecfa1415134151b8.mp3"
    arcardy "Пожалуй; только он, право, хороший человек."

    voice "voice/bazarov/0fcee03c37f8e58d.mp3"
    bazarov "Архаическое явление! А отец у тебя славный малый. Стихи он напрасно читает и в хозяйстве вряд ли смыслит, но он добряк."

    voice "voice/arcardy/917b42ed874b9e39.mp3"
    arcardy "Ты про Фенечку знаешь?"

    voice "voice/bazarov/50aaaec0a5736e3f.mp3"
    bazarov "{i}(пожимает плечами){/i} Дамы в этом доме — на вес воды. Ни одна не оглянулась. Скучно."

    voice "voice/arcardy/afd43ad790060a44.mp3"
    arcardy "Одна оглянулась, да не на тебя. На меня. Катя."

    voice "voice/bazarov/43c6c9da1c50997e.mp3"
    bazarov "{i}(встаёт){/i} Ну, голубчик, это не моё дело. Я пойду светиться: лягушку надо выпотрошить, а у тебя тут…"
    "{i}(он оглядывает комнату и не договаривает){/i}"

    $ play_narrator("19c653b288749935")
    "Базаров уходит. Дверь хлопает; в комнате становится тихо."

    stop music fadeout 2.0

    jump scene_2b


# ============================================================
# СЦЕНА 2b. История Павла Петровича (глава V)
# ============================================================
label scene_2b:

    call chapter_card("ГЛАВА V", "История одного брата") from _card2b

    scene maryino_room at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 2.0 volume 0.35

    $ play_narrator("70cab59db44c76ed")
    "Две ночи спустя. Аркадий не спит, и в его комнату заходит Николай Петрович."

    show nikolaydef at left_char
    with dissolve
    show arcardiydef at right_char
    with dissolve

    voice "voice/nikolay/76b1b7f9d95d65b0.mp3"
    nikolay "{i}(садится, долго не начинает){/i} Ты хотел знать историю Павла… Я расскажу. Всё равно рано или поздно, а при Базарове я бы не смог."

    voice "voice/arcardy/0a020e42f0cece0b.mp3"
    arcardy "Папаша, я слушаю."

    voice "voice/nikolay/c6effb24b8a3a491.mp3"
    nikolay "Он мог быть… ты не поверишь… он мог быть велик. Свет его знал. В тридцать лет он дослужился до капитана и был красавец из красавцев."

    "{i}(Николай Петрович смотрит на окно, за которым ещё чернеет ночь.){/i}"
    voice "voice/nikolay/c7f2e5db8aafdc9e.mp3"
    nikolay "Была одна женщина — княгиня Н. П. Она была нехороша собой, но… есть в ней что-то, от чего теряют голову. Она знала, что он не сможет жить без неё, и не допускала его к себе. Давала надежду — и отнимала. Месяц — и ни одного шага вперёд."

    voice "voice/arcardy/d479325ff6d1c611.mp3"
    arcardy "И он?"

    voice "voice/nikolay/8b7a7bcba3c4d721.mp3"
    nikolay "И он играл на бирже, проигрался, отдал всё, что имел, расплатился за неё… и не покорился."
    voice "voice/nikolay/ea19873113637d01.mp3"
    nikolay "Она вышла замуж за другого, за старого генерала. Он уехал в действующую армию, в камчатский полк, прошёл всю войну, вышел в отставку — и приехал ко мне. С тех пор вот двадцать два года он живёт один."

    menu:
        "«Отчего же он никогда об этом не говорит?»":
            $ pavel_history = True
            $ kinship += 1
            voice "voice/arcardy/2988747b2b086037.mp3"
            arcardy "Отчего он никогда об этом не говорит, папаша?"
            voice "voice/nikolay/e81efd48d4d20848.mp3"
            nikolay "Говорил. Один раз, на третьем году после её смерти. А потом перестал… Он её до сих пор любит, Аркаша. Ты заметь: у него всё в дому, в костюме, в привычках — из той жизни. Он не живёт, он служит памяти."
            "{i}(Аркадий молчит впервые в жизни так долго.){/i}"
        "«Бедный дядюшка» — сказать и обнять отца":
            $ pavel_history = True
            $ mercy += 1
            voice "voice/arcardy/59cfcf7960483e35.mp3"
            arcardy "Бедный дядюшка… И бедный ты, папаша: ты-то всё это помнишь и всё это носишь."
            "{i}(Николай Петрович вскакивает, хочет сказать что-нибудь остроумное, не находит, обнимает сына и уходит молча.){/i}"
            $ play_narrator("10a4cc24d90e2388")
            "На пороге он всё-таки останавливается."
            voice "voice/nikolay/4948544053ce9843.mp3"
            nikolay "{i}(тихо){/i} И запомни: никому из них. Ни Базарову, ни Павлу. Он не простит."
        "Спросить про Фенечку, пока отец не ушёл":
            $ pavel_history = True
            $ kinship += 1
            voice "voice/arcardy/d5ebd73ab943c213.mp3"
            arcardy "Папаша… а Фенечка? Это то, что я думаю?"
            "{i}(Николай Петрович краснеет до ушей, но не отводит глаз.){/i}"
            voice "voice/nikolay/c3533ba1164163a9.mp3"
            nikolay "Это… это, Аркаша, моя слабость. И моя жизнь. Ты увидишь её завтра — и не суди меня."
            voice "voice/arcardy/f29dda5db674e9ec.mp3"
            arcardy "Я тебя не сужу. Я тебя люблю, папаша."
            voice "voice/nikolay/b4a45e20747397ae.mp3"
            nikolay "{i}(садится на край кровати и закрывает лицо руками){/i} Ну, вот и всё. Вот и поговорили… Ступай спать, а то Павел Петрович увидит, что у нас свет."

    hide nikolaydef
    hide arcardiydef
    with dissolve

    "{i}(Аркадий ещё долго лежит без свечи. Внизу, в кабинете Павла Петровича, тоже горит огонь.){/i}"

    $ play_narrator("cc237aac5cf1a4f9")
    "Рассказ о человеке, который двадцать два года носит в кармане чужое письмо и не перечитывает его, переменяет в Аркадии что-то, чего он ещё не умеет назвать."

    stop music fadeout 2.5

    jump scene_3


# ============================================================
# СЦЕНА 3. Фенечка и тайна Николая (главы VI–VIII)
# ============================================================
label scene_3:

    call chapter_card("ГЛАВА VI–VIII", "Утро в Марьине") from _card3

    scene maryino_morning at bg_kb
    with fade

    play music "music/light-breeze.ogg" fadein 1.5 volume 0.5

    $ play_narrator("b6437cb0742f60a9")
    "Утро. Терраса залита мягким солнечным светом. На столе самовар, большие букеты сирени."
    $ play_narrator("0b9f3ab9b1e13b8e")
    "Николай Петрович нервно разливает чай. Из боковой комнаты доносится тихий детский лепет. Фенечка не выходит — она стесняется."

    show nikolaydef at right_char
    with dissolve
    show arcardiydef at left_char
    with dissolve

    voice "voice/arcardy/c38b64ab9787911b.mp3"
    arcardy "{i}(опустив глаза){/i} Папаша… Извини, если мой вопрос тебе покажется неуместным… Но ты сам вчерашнею своею откровенностью меня вызываешь на откровенность… Не оттого ли Фен… не оттого ли она не приходит сюда чай разливать, что я здесь?"

    "{i}(Николай Петрович смущённо отворачивается и краснеет.){/i}"
    voice "voice/nikolay/3e7cd66cd4639b28.mp3"
    nikolay "Может быть… она предполагает… она стыдится…"

    voice "voice/arcardy/662c9563a3565eee.mp3"
    arcardy "Напрасно ж она стыдится! Во-первых, тебе известен мой образ мыслей… а во-вторых — захочу ли я хоть на волос стеснять твою жизнь, твои привычки?"
    voice "voice/arcardy/98cb1616e1f702c8.mp3"
    arcardy "Притом я уверен, ты не мог сделать дурной выбор. Если ты позволил ей жить с тобой под одной кровлей, стало быть, она это заслужила. Сын отцу не судья… и в особенности такому отцу, который никогда и ни в чём не стеснял моей свободы."

    "{i}(Николай Петрович глухо потирает лоб.){/i}"
    voice "voice/nikolay/2907cb7d9bc078f4.mp3"
    nikolay "Спасибо, Аркаша… Твои предположения действительно справедливы. Конечно, если б эта девушка не стоила… Это не легкомысленная прихоть…"
    voice "voice/nikolay/f694ae5243773e9a.mp3"
    nikolay "Мне неловко говорить с тобой об этом, но ты понимаешь: ей трудно было прийти сюда при тебе, особенно в первый день."

    voice "voice/arcardy/2faf0183f40268cf.mp3"
    arcardy "Так вели её позвать. Сейчас. Сегодня. Иначе я сам пойду и приведу её за руку."

    menu:
        "Идти самому и привести Фенечку к столу":
            $ mercy += 1
            $ kinship += 1
            $ play_narrator("872c12482ce6c934")
            "Аркадий встаёт, идёт через гостиную и стучит в боковую дверь. Ему отвечают не сразу — и он возвращается не один."
            "{i}(Фенечка входит в лёгком летнем платье, с опущенными глазами, и садится у стола так тихо, точно её и нет.){/i}"
            voice "voice/fedosiya/7594ea10db62656f.mp3"
            fedosiya "{i}(еле слышно){/i} Помилуйте, Аркадий Николаич… я ведь простая… вы со мной не знайтеся."
            voice "voice/arcardy/08a3638007caab46.mp3"
            arcardy "Я, Федосья Николаевна, всю дорогу от Петербурга прожил с человеком, который про простые вещи говорит умнее всех нас."
        "Оставить отца одного и уйти в сад, где Базаров чистит ножи":
            $ nihil += 1
            hide arcardiydef
            hide nikolaydef
            show bazarovdef at left_char
            with dissolve
            show arcardiydef at right_char
            with dissolve
            voice "voice/bazarov/7180b14a8230dbae.mp3"
            bazarov "{i}(не поднимая головы){/i} Ну что, студент? Пошёл человека судить или простил?"
            voice "voice/arcardy/4197fffc36b7b0dc.mp3"
            arcardy "Я не пошёл."
            voice "voice/bazarov/ea6faed48406717d.mp3"
            bazarov "И хорошо сделал. Сентиментальность — та же болезнь, только заразная."

    hide bazarovdef
    hide arcardiydef
    hide nikolaydef

    $ play_narrator("0c4c7adc73aec51b")
    "Час спустя Аркадий возвращается сияющий."

    show nikolaydef at right_char
    with dissolve
    show arcardiydef at left_char
    with dissolve

    voice "voice/arcardy/1da4ba04b4abe402.mp3"
    arcardy "{i}(торжествующе){/i} Мы познакомились, отец! Федосья Николаевна точно сегодня не совсем здорова и придёт попозже."
    voice "voice/arcardy/2c71640875f21135.mp3"
    arcardy "Но как же ты не сказал мне, что у меня есть брат? Я бы уже вчера вечером его расцеловал, как я сейчас расцеловал его!"

    "{i}(Николай Петрович растроганно обнимает сына.){/i}"
    voice "voice/nikolay/42fb0ac9a2b66e7c.mp3"
    nikolay "Аркадий…"

    $ play_narrator("d0c20b8799212fac")
    "Митя, услышав новые голоса, выбегает на террасу и тянет руки к сирени."

    voice "voice/mitya/3f43340fae833fa2.mp3"
    mitya "Ма! Ба-ба-ба!"

    voice "voice/arcardy/7bfa07bb00f773a9.mp3"
    arcardy "{i}(подхватывает его){/i} Вот это по-нашему! Настоящий маленький материалист: хочет — и берёт."

    hide arcardiydef
    hide nikolaydef

    $ play_narrator("07f86d00fd8df898")
    "Позже Павел Петрович заходит к Фенечке."

    show paveldef at left_char
    with dissolve
    show fedosiyadef at right_char
    with dissolve

    voice "voice/pavel/201f13f668e41ea2.mp3"
    pavel "Извините, если я помешал… Мне хотелось только попросить вас… сегодня, кажется, в город посылают… велите купить для меня зелёного чаю. Полфунта довольно будет, я полагаю."

    voice "voice/fedosiya/7fa147c56c567903.mp3"
    fedosiya "Слушаю-с… Сколько прикажете купить?"

    voice "voice/pavel/ffd2a17b1f602ddf.mp3"
    pavel "А у вас здесь, я вижу, перемена… Занавески вот."

    voice "voice/fedosiya/c752add1ef28ad95.mp3"
    fedosiya "Да-с, занавески… Николай Петрович нам их пожаловал. Да уж они давно повешены."

    voice "voice/pavel/2e54e809d3473273.mp3"
    pavel "Вам здесь лучше, чем в прежнем флигельке?"

    voice "voice/fedosiya/9a918b9040357183.mp3"
    fedosiya "Конечно, лучше-с."

    voice "voice/pavel/c8f28508dc6ef3a6.mp3"
    pavel "Отчего вы велели вашего маленького вынести? Я люблю детей. Покажите-ка мне его."

    "{i}(Фенечка краснеет от радости.){/i}"
    voice "voice/fedosiya/1877ca7b68b7931d.mp3"
    fedosiya "Дуняша… принесите Митю…"

    voice "voice/dunyasha/63c493a144a0c3d3.mp3"
    dunyasha "{i}(из-за двери){/i} Сейчас-с, Павел Петрович. Только его укачивать надо, он не спал ночь."

    $ play_narrator("81fe1a38afb84bb5")
    "Фенечка передаёт ребёнка. Павел Петрович щекочет подбородок Мити длинным ногтем."

    voice "voice/pavel/434c8161a90ec438.mp3"
    pavel "Экой бутуз… Он похож на брата. Несомненное сходство."

    "{i}(Он поднимает глаза на Фенечку — и в эти глаза входит то, чего он сам не ждал.){/i}"

    voice "voice/pavel/b7149260c3dcdcb5.mp3"
    pavel "{i}(совсем другим тоном){/i} Вы… вы, верно, скучаете, Федосья Николаевна. Книг у вас нет? У меня в кабинете есть… я прикажу принести."

    voice "voice/fedosiya/37eb2036d868b211.mp3"
    fedosiya "{i}(тихо){/i} Помилуйте, Павел Петрович, какие ж книги… Мне с Митей да с хозяйством довольно."

    voice "voice/pavel/84aa66955b83b656.mp3"
    pavel "{i}(встаёт, неловко){/i} Да… Конечно. Чай… не забудьте."

    show nikolaydef at side_char
    with dissolve

    $ play_narrator("daceb57729289e7a")
    "В дверях появляется Николай Петрович и видит эту сцену."

    "{i}(Братья смотрят друг на друга через комнату, через ребёнка, через Фенечку — и оба понимают всё без единого слова.){/i}"

    if pavel_history:
        "{i}(Аркадий, вспомнив отцов рассказ, останавливается у притолки и думает вслух.){/i}"
        voice "voice/arcardy/7f96fdfa4190a6a1.mp3"
        arcardy "{i}(про себя){/i} Боже мой… он ведь опять."
    else:
        "{i}(Аркадий, входя следом за отцом, останавливается на середине комнаты.){/i}"
        voice "voice/arcardy/d368599d48728541.mp3"
        arcardy "{i}(про себя){/i} Что с дядей? Он ни на кого так не глядел."

    hide paveldef
    hide fedosiyadef
    with dissolve

    show arcardiydef at right_char
    show nikolaydef at left_char
    with dissolve

    "{i}(Николай Петрович берёт сына под локоть и выводит его в сени, где пахнет свежим сеном и воском.){/i}"
    voice "voice/nikolay/cca435decba31615.mp3"
    nikolay "{i}(вполголоса){/i} Скажи ему… скажи Базарову, чтобы он перестал ездить к ней. Я не смею просить, я не имею права… Ты имеешь."
    voice "voice/arcardy/1db3c8accf86261b.mp3"
    arcardy "Папаша, он и так уезжает в Васильевку. Завтра."
    voice "voice/nikolay/9c4b5fc634a5febd.mp3"
    nikolay "{i}(садится на ступеньку, держась за козырёк){/i} Завтра. Вот и хорошо. Завтра. А после завтра — посмотрим, кто из нас двоих здесь хозяин."
    "{i}(Он усмехается своей шутке и тут же перестаёт: шутка была правдой.){/i}"

    hide paveldef
    hide fedosiyadef
    hide nikolaydef
    hide arcardiydef
    with dissolve

    $ play_narrator("63226a50f5b9ad9c")
    "Вечером к террасе подъезжает коляска: из города приехали Лиза, свояченица Анны Сергеевны, и её младшая сестра Катя."

    show catyadef at side_right_char
    with dissolve

    "{i}(Катя, лет тринадцати, в белом платьице, стоит у перил и смотрит на воду, никого не видя.){/i}"

    voice "voice/liza/26d7f56c5f5cf582.mp3"
    liza "{i}(Лиза, входя следом, смеётся){/i} Аркадий Николаич, вы обещали нам Базарова, а не себя. Где же чудовище?"

    menu:
        "Подойти к Кате и заговорить о ней, а не о сестре":
            $ kinship += 1
            show arcardiydef at right_char
            with dissolve
            voice "voice/arcardy/5eefe7ce9b9955ca.mp3"
            arcardy "Вы, я вижу, не любите танцевать. Я тоже. Я бы всю жизнь просидел у воды, если б мне позволили."
            voice "voice/catya/3347657a70204864.mp3"
            catya "{i}(удивлённо, серьёзно не по годам){/i} А разве можно всю жизнь просидеть у воды? Надо же чем-то быть нужным."
            voice "voice/arcardy/365cba7b632daa6c.mp3"
            arcardy "{i}(смущается, и ему это нравится){/i} Можно… кажется, можно."
        "Сказать любезности Лизе, как принято между приятелями":
            $ nihil += 1
            show arcardiydef at right_char
            with dissolve
            voice "voice/arcardy/5c65ffa80effd54e.mp3"
            arcardy "Вы нас удивили, Лизавета Николаевна. Мы ждали вас только к обеду."
            voice "voice/catya/76fbe8623526be71.mp3"
            catya "{i}(тихо сестре){/i} Он говорит, как в театре."
            $ play_narrator("9ade67ded2c865be")
            "Лиза смеётся во всё горло, а Катя не смеётся и смотрит в воду."

    hide catyadef
    hide arcardiydef

    stop music fadeout 2.0

    jump scene_4


# ============================================================
# СЦЕНА 4. Ситников, Козьин, бал и Никольское (главы IX–XVII)
# ============================================================
label scene_4:

    call chapter_card("ГЛАВА IX–XI", "Молодые люди") from _card4

    scene maryino_terrace at bg_kb
    with fade

    play music "music/light-breeze.ogg" fadein 1.0 volume 0.5

    $ play_narrator("fbf264049611eb9f")
    "Июнь. К крыльцу Марьина подкатывает фаэтон, в котором сидят два неизвестных."

    show bazarovdef at left_char
    with dissolve
    show arcardiydef at right_char
    with dissolve

    $ play_narrator("0f8116f94738aae0")
    "Из фаэтона вылезает худощавый молодой человек в летнем пальто на четырёх пуговицах, в клетчатых брючках и круглой шляпе; за ним — коренастый, рыжий, молчаливый."

    voice "voice/smit/b87b853de04b3422.mp3"
    smit "{i}(тараторя, с расстановкой){/i} Очень, очень рад! Я так и думал застать вас. Мы с Козьиным приехали на вашу переправу, а Козьин — он человек положительный, он вам сыграет…"

    voice "voice/kozy/3dfb3fbe2010d2b9.mp3"
    kozy "{i}(раскланивается один раз и на всё){/i} Честь имею."

    voice "voice/bazarov/f955a48fdc9a70ba.mp3"
    bazarov "{i}(Аркадию, вполголоса){/i} Это Ситников. Он ездит ко мне учиться. Он будет нашим последователем, как все они."

    $ play_narrator("60da7eca5a8af706")
    "Козьин вынимает из фаэтона скрипку и, ничего не отвечая на вопросы, начинает играть — вальс, потом польку, потом что-то, чего никто не знает."

    voice "voice/smit/5927aabc1ef2e320.mp3"
    smit "{i}(подмигивая){/i} Он это называет «философически». У него есть теория: всё, что играется, должно быть похоже на то, что думаешь."

    menu:
        "Засмеяться открыто, как смеются над чужими":
            $ nihil += 1
            voice "voice/arcardy/e8c6473fd646308b.mp3"
            arcardy "{i}(не удержавшись, хохочет){/i} Простите! Это невозможно! Это… это на что-то похоже, но я не могу сказать на что."
            voice "voice/smit/f5f8d32d3d542574.mp3"
            smit "{i}(обидчиво){/i} Ha! Смешно! А между тем это очень тонко. Вы, Аркадий Николаич, ещё не понимаете. Это — впечатление, а не звук. Базаров, скажите ему!"
            voice "voice/bazarov/977703cf1915f465.mp3"
            bazarov "{i}(холодно){/i} Аркадий смеётся потому, что ему хочется смеяться. Смейся, мой друг, это ни к чему не обязывает."
            "{i}(Через час Базаров отзовёт Аркадия в сторону.){/i}"
            voice "voice/bazarov/51f8e0c8770cc718.mp3"
            bazarov "Ты смеялся. Зря. Они не смешные, они бедные. А бедное не смешно, когда у тебя нет права на смех."
            $ mercy += 1
        "Смеяться втихомолку, но не показать Базарову":
            $ kinship += 1
            "{i}(Аркадий отворачивается к перилам и смеётся одними плечами.){/i}"
            voice "voice/smit/65b7c3aac7e8f8bd.mp3"
            smit "{i}(не замечая){/i} Правда, хорошо? Козьин четыре года учился у одного немца в уездном городе, и тот ему сказал: «Ты имеешь чувство». Больше он ничего не говорил — и Козьин счастлив."
            "{i}(Козьин кланяется на похвалу и играет ещё усерднее.){/i}"
        "Слушать серьёзно до конца":
            $ mercy += 1
            $ kinship += 1
            "{i}(Аркадий слушает, не двигаясь. Вальс нескладен, фальшив, но в нём есть что-то упорное, почти трогательное.){/i}"
            voice "voice/arcardy/bb7d8d4001a500df.mp3"
            arcardy "{i}(когда скрипка смолкает){/i} У него верная рука. Не то чтобы талант — а верная рука."
            voice "voice/kozy/ddce8fa0d5671abe.mp3"
            kozy "{i}(расцветая, басом){/i} С-спасибо, сударь. Четыре года."
            voice "voice/bazarov/2aca7bc37131f2ec.mp3"
            bazarov "{i}(в сторону){/i} Ну, брат, ты сегодня лучше, чем вчера. Тебе бы в защитники бедных, а не в нигилисты."
        "Заступиться за Пушкина — вслух, перед всеми":
            $ speta_branch = True
            jump scene_4_speta

    label story_after_sitnikov:

    # возврат из новой ветки: та же терраса, что стояла до jump
    scene maryino_terrace at bg_kb
    with dissolve

    hide bazarovdef
    hide arcardiydef
    with dissolve

    $ play_narrator("56e119f16271e350")
    "Ситников и Козьин уезжают к пяти часам: Ситникову надо поспеть к невесте, у которой, по его выражению, «положительные» понятия о браке."

    stop music fadeout 2.0

    call chapter_card("ГЛАВА XII–XV", "Губернский бал") from _card4b

    scene ball at bg_kb
    with fade

    play music "music/waiting_theme.ogg" fadein 2.0 volume 0.7

    $ play_narrator("289a40fa6ae8192e")
    "Губернский бал. Яркие огни, музыка, кружащиеся пары."
    $ play_narrator("cbddf686fce4fd7f")
    "Анна Сергеевна Одинцова стоит в центре зала — высокая, спокойная, в строгом платье. Её взгляд холоден и притягателен одновременно."

    show annadef at right_char
    with dissolve
    show arcardiydef at left_char
    with dissolve

    "{i}(Базаров стоит сзади, скучающе, с тем видом, с каким на балах стоят врачи.){/i}"

    menu:
        "Пригласить Одинцову и говорить о ней, а не о себе":
            $ anna_open += 2
            $ kinship += 1
            voice "voice/anna/b91396afa5c43245.mp3"
            anna "{i}(Аркадию){/i} Вы обещали мне посетить меня. Привезите же с собой и вашего приятеля. Я буду рада."
            voice "voice/arcardy/5fd0c1003565ef34.mp3"
            arcardy "Он приедет. Только он… он не умеет на балах. Он умеет говорить, и то не всегда вовремя."
            voice "voice/anna/b19f9644021e4bb8.mp3"
            anna "{i}(улыбается){/i} Мне это не мешает. Мне мешает только скука. А он не скучен."
            $ play_narrator("7a81184c6836edf1")
            "Анна Сергеевна смотрит поверх головы Аркадия на Базарова — и Базаров впервые на бале не отводит глаза."
        "Сказать прямо: «Он вас разлюбит, если вы будете с ним ласковы»":
            $ anna_open += 1
            $ nihil += 1
            voice "voice/arcardy/ea1e3b9f7317975e.mp3"
            arcardy "{i}(вспыхнув от собственной смелости){/i} Анна Сергеевна… Он вас разлюбит, если вы будете с ним ласковы. Или полюбит. Я не знаю, что хуже."
            voice "voice/anna/568f0afa113902d2.mp3"
            anna "{i}(долгий взгляд, ровный голос){/i} Вы слишком много говорите о другом, Аркадий Николаич. Это признак… не скромности."
            voice "voice/arcardy/d51397281707ced6.mp3"
            arcardy "Это признак дружбы."
            voice "voice/anna/4627103e0597a159.mp3"
            anna "{i}(чуть заметно){/i} Тогда я запомню. Но я никого не боюсь, кроме дурной музыки. А её, кажется, сейчас кончают."
        "Оттанцевать мазурку с Катей и не смотреть на Одинцову":
            $ kinship += 2
            $ play_narrator("18019fd02e4ab51d")
            "Аркадий приглашает Катю. Они не говорят ни о чём; музыка кончается слишком скоро."
            voice "voice/catya/5c04fc629562663f.mp3"
            catya "{i}(уходя с круга){/i} Вы сегодня не похожи на себя. У вас не то лицо, что в Марьине."
            voice "voice/arcardy/df172a5d61553e48.mp3"
            arcardy "{i}(про себя){/i} Какое же у меня лицо в Марьине?"
            "{i}(Анна Сергеевна замечает, что молодой Кирсанов не подошёл к ней весь вечер, и это её занимает.){/i}"
            $ anna_open += 1

    hide arcardiydef
    hide annadef
    hide bazarovdef

    $ play_narrator("5bbc16f8d22b5827")
    "На другой день Базаров едет один в Никольское — за грибами, за разговором, за тем, чего не умеет назвать."

    call chapter_card("ГЛАВА XVI–XVII", "Никольское") from _card4c

    scene nikolskoe at bg_kb
    with fade

    stop music fadeout 1.5
    play music "music/light-breeze.ogg" fadein 1.5 volume 0.45

    $ play_narrator("fe7ea4ce61ffd4a3")
    "Никольское. Вечер в гостиной. Свечи, тишина, запах духов и старых книг."

    show annadef at right_char
    with dissolve
    show bazarovdef at left_char
    with dissolve

    voice "voice/bazarov/682472989c271b9b.mp3"
    bazarov "{i}(глядя прямо){/i} С вашей красотою живёте в деревне? Это странно."

    voice "voice/anna/8b16e15b0ffc2264.mp3"
    anna "Как? Как вы это сказали?"

    voice "voice/bazarov/e8dff76983953a9e.mp3"
    bazarov "Я сказал: странно. Вы могли бы жить в Петербурге и делать там что хотите."

    voice "voice/anna/7b7c5c7d36ae95a5.mp3"
    anna "{i}(садится, не отвечая сразу){/i} Я пробовала. В Петербурге все хотят от меня чего-то, и никто не говорит со мной. Здесь я хотя бы знаю, чего хочу."

    voice "voice/bazarov/60ed5694cda202c8.mp3"
    bazarov "И чего же?"

    voice "voice/anna/c43a7770b44c919c.mp3"
    anna "Спокойствия. Я его берегу, как берегут богатство. Вы, верно, скажете: буржуазная добродетель."

    voice "voice/bazarov/4e4cd145c2ea1035.mp3"
    bazarov "{i}(садится напротив, подвинув стул ближе, чем надо){/i} Нет. Я скажу: разумная. Только она не вечна. Спокойствие — это как покой в трупе: тело ещё тёплое, а уже ничего нет."

    voice "voice/anna/46f2c69401758bb5.mp3"
    anna "{i}(не отводя глаз){/i} Вы всегда так говорите — или только когда вам смешно?"

    $ play_narrator("06e7c2a81fdd0f41")
    "Долгий разговор о науке и жизни. За окнами темнеет. Базаров говорит всё резче, словно злится на самого себя."

    if anna_open >= 2:
        $ play_narrator("25d5d8c87c419e21")
        "Анна Сергеевна внимательна. Она подаёт ему слово за словом, и он подхватывает их — как человек, который идёт по реке и не хочет заметить, что течение уже сильное."
    else:
        $ play_narrator("8ee4672f7314ef9b")
        "Анна Сергеевна отвечает холодно и коротко. Базаров злится, и злость раззадоривает его ещё больше."

    menu:
        "Сказать всё до конца, не оглядываясь":
            $ bazarov_spoke_all = True
            $ anna_open += 1
            voice "voice/bazarov/d3842bf771c787bd.mp3"
            bazarov "{i}(внезапно, резко){/i} Я люблю вас, глупо, безумно… Вот чего вы добились."
            "{i}(Анна Сергеевна спокойна, но в её голосе дрожь.){/i}"
            voice "voice/anna/ad5cb20f5647a461.mp3"
            anna "Вы не могли сказать это серьёзно."
            voice "voice/bazarov/7f1c10aa9dee9d86.mp3"
            bazarov "Я говорю серьёзно. Вы этого хотели — вы получили."
            voice "voice/anna/12e4ab0fafe24213.mp3"
            anna "Но зачем? Зачем вы это говорите?"
            voice "voice/bazarov/b0e6bf2c4a955819.mp3"
            bazarov "Зачем? Чтобы вы знали. Чтобы вы поняли, что я не шучу. Я не умею иначе: или всё, или ничего."
            voice "voice/anna/1d469d8fe6b3d4f0.mp3"
            anna "{i}(встаёт, отходит к окну){/i} Я не могу вам ответить. И, кажется, никогда не смогу. Вы сорвёте меня с места, а мне нужно место."
            voice "voice/bazarov/6989b28b988955c5.mp3"
            bazarov "{i}(тоже встаёт){/i} Тогда я уеду. И не приеду. Это будет, как если б я ничего не говорил."
            voice "voice/anna/eb3b9f73f8cfa161.mp3"
            anna "{i}(тихо){/i} Нет. Скажите, что вы не ехали в Никольское за грибами."
            $ play_narrator("33d884fcc10486c2")
            "Оба замолкают. Где-то в соседней комнате тихо перебирают клавиши."
        "Остановиться на полуслове и перевести на шутку":
            voice "voice/bazarov/2ce709185e75aae0.mp3"
            bazarov "{i}(начинает и обрывает себя; в комнате становится тихо оттого, что он не договаривает){/i} Я… к чёрту. Не берите в голову. У вас тут чай плохой."
            voice "voice/anna/3b6c54ad56fff44e.mp3"
            anna "{i}(замечает всё){/i} Вы хотели сказать что-то другое, и я слышала начало. Я не стану спрашивать."
            voice "voice/bazarov/7ee1b1a43fda0c23.mp3"
            bazarov "{i}(усмехается, но усмешка кривая){/i} Вот это и есть настоящая жестокость: не спрашивать."
            voice "voice/anna/3ac7c06e0f0bfcab.mp3"
            anna "Я берегу спокойствие, Евгений Васильевич. Вы сами меня в этом похвалили."
            voice "voice/bazarov/d28503650d3b63da.mp3"
            bazarov "{i}(встаёт, надевает фуражку, не прощаясь){/i} Спокойствие. Да. Хорошее слово, чтобы похоронить в нём живого человека."
            "{i}(Дверь за ним затворяется мягко, без стука. Анна Сергеевна сидит ещё долго и не передвигает ни одной книги на столе.){/i}"
            $ anna_open += 1

    hide annadef
    hide bazarovdef

    $ play_narrator("190e261568a39568")
    "На следующий день, перед отъездом."

    show bazarovdef at left_char
    with dissolve
    show arcardiydef at right_char
    with dissolve

    if bazarov_spoke_all:
        voice "voice/bazarov/ad1da15a7608fecb.mp3"
        bazarov "Всё кончено. Я уезжаю. Она меня отвергла. То есть нет… она меня не отвергла. Она меня не взяла. Это хуже."
        voice "voice/arcardy/5f50d3cc73bb0518.mp3"
        arcardy "Евгений…"
        voice "voice/bazarov/c0f1d7977311d8f0.mp3"
        bazarov "{i}(оскаляется){/i} Не говори ничего. Мне хочется тебя ударить, а я тебя люблю, как единственного. Вот и сиди молча."
    else:
        voice "voice/bazarov/31129f6dda891683.mp3"
        bazarov "Всё кончено. Я уезжаю. Она меня не услышала. А может, услышала и не захотела."
        voice "voice/arcardy/057ebb9e3205f29d.mp3"
        arcardy "Ты ведь почти не сказал ей ничего."
        voice "voice/bazarov/98ad387e56ddc432.mp3"
        bazarov "{i}(резко){/i} Довольно, Аркадий. Разговор окончен. Запомни одно: не играй с огнём, если у тебя карман бумажный."

    $ play_narrator("34d3c46c106cb89e")
    "Базаров и Аркадий возвращаются в Марьино. Всю дорогу Базаров угрюмо молчит."

    stop music fadeout 2.0

    jump scene_5


# ============================================================
# СЦЕНА 5. Ночь перед дуэлью (главы XVIII–XX)
# ============================================================
label scene_5:

    call chapter_card("ГЛАВА XVIII–XIX", "Ночь перед рассветом") from _card5

    scene maryino_room at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 1.5 volume 0.5

    $ play_narrator("ff004df49928196d")
    "Ночь. В кабинете Павла Петровича горит лампа. Он сидит, не раздеваясь, с бумагой в руке."

    show paveldef at center_char
    with dissolve

    voice "voice/pavel/db7d48d3d9892b65.mp3"
    pavel "{i}(про себя, пера не берёт){/i} «…и потому прошу вас, милостивый государь, более не заезжать к Федосье Николаевне…»"
    "{i}(Он читает написанное вслух, и голос у него не ровный.){/i}"
    voice "voice/pavel/1607b155ffdc1342.mp3"
    pavel "Нелепо. По-французски было бы лучше, но по-французски он не поймёт. Он поймёт по-русски: он всё понимает, когда дело до женских юбок."

    "{i}(В коридоре скрипит половица. Павел Петрович сворачивает записку и кладёт её под пресс-папье — на видное место.){/i}"

    hide paveldef

    $ play_narrator("d3bc3df547345ce6")
    "Утром Аркадий находит записку. Он знает, чья рука, и знает, что прочтёт её тот, кому она не послана."

    menu:
        "Отнести письмо Николаю Петровичу, как есть":
            $ duel_warned = True
            $ mercy += 1
            $ kinship += 1
            show nikolaydef at right_char
            with dissolve
            "{i}(Аркадий кладёт письмо перед отцом и отворачивается.){/i}"
            voice "voice/nikolay/779526e2f3b00d63.mp3"
            nikolay "{i}(читает, бледнеет, перечитывает){/i} Это… это Павел? Кому он это пишет…"
            voice "voice/arcardy/2154f6f9066a416a.mp3"
            arcardy "Базарову, папаша."
            voice "voice/nikolay/256160e13d305a50.mp3"
            nikolay "{i}(встаёт, у него дрожат руки){/i} Нет. Нет, этого не будет. Я сам поеду к губернатору, я… я напишу, я…"
            voice "voice/arcardy/2c66be2336f43fc0.mp3"
            arcardy "Уже поздно. Павел Петрович сегодня утром отправил секунданту в город."
            voice "voice/nikolay/bedd1f2d815a5e6d.mp3"
            nikolay "{i}(садится тяжело){/i} Аркаша… это из-за меня. Из-за меня всё это. Пойди к нему… к обоим… пока не рассвело."
            hide nikolaydef
            "{i}(Николай Петрович посылает Прокофьича за Базаровым, но поздно: вызов уже принят, и отговорить Павла Петровича не смог бы теперь никто.){/i}"
            show paveldef at center_char
            with dissolve
            voice "voice/pavel/cba45d304b234f4a.mp3"
            pavel "{i}(завязывая перчатки, спокойно){/i} Я всё решил, братец. И ты меня не удержишь. Мне двадцать два года хочется одного: чтобы хоть раз в жизни вышло по-честному."
            hide paveldef
        "Спрятать письмо и идти к Базарову, чтобы удержать его":
            $ duel_warned = True
            $ mercy += 1
            $ nihil += 1
            show bazarovdef at right_char
            with dissolve
            "{i}(Аркадий находит Базарова в саду, с ножом и лягушкой.){/i}"
            voice "voice/arcardy/7c22e11e14373aaa.mp3"
            arcardy "Уходи, Евгений. Сегодня. Не отвечай, не пиши, уезжай к себе в Васильевку."
            voice "voice/bazarov/9f9db877b33ac097.mp3"
            bazarov "{i}(не поднимая головы){/i} Ты про что?"
            voice "voice/arcardy/dd4fa02e2cf7f4ae.mp3"
            arcardy "Про то, что Павел Петрович написал тебе письмо, а я его читал. И он послал своего секунданта."
            voice "voice/bazarov/0a0f3bf1a33372ef.mp3"
            bazarov "{i}(откладывает нож, медленно){/i} Так. Ну и что ж — ты хочешь, чтобы я струсил?"
            voice "voice/arcardy/723a5dfc1d0eb574.mp3"
            arcardy "Хочу, чтобы ты остался жив. Он-то тебя не убьёт, он не умеет. А ты его — можешь."
            voice "voice/bazarov/bd44cb0c9fcba519.mp3"
            bazarov "{i}(встаёт, вытирает руки о пальто){/i} Аркадий… Ты меня уважаешь?"
            voice "voice/arcardy/f2075d8dfb0750f9.mp3"
            arcardy "Больше всех."
            voice "voice/bazarov/6d93f8c7a90f062a.mp3"
            bazarov "Тогда не мешай. Я не пойду стреляться из-за Фенечки — это была бы комедия. Я пойду, потому что он послал записку, а на записку отвечать иначе нельзя. Понимаешь ты это, студент, или нет?"
            "{i}(Аркадий понимает и молчит.){/i}"
            hide bazarovdef
        "Не трогать письмо и выйти в сад":
            $ play_narrator("2e9ef08fd1fcf946")
            "Аркадий кладёт бумагу ровно так, как нашёл, и уходит. Он говорит себе, что это не его дело, что они взрослые, что всё кончится вздором."
            "{i}(За окном ещё темно, и в темноте он слышит, как по кабинету Павла Петровича кто-то ходит туда и обратно, не останавливаясь, — очень долго.){/i}"

    call scene_5_duel from _duel

    jump scene_5b


# ============================================================
# СЦЕНА 5d. Дуэль (главы XXI–XXIV)
# ============================================================
label scene_5_duel:

    call chapter_card("ГЛАВА XXII–XXIV", "Дуэль") from _card5d

    scene garden_duel at bg_kb
    with fade

    play sound "sounds/tree-creak.ogg"
    play music "music/waiting_theme.ogg" fadein 1.0 volume 0.9

    $ play_narrator("092917f245cfeb20")
    "Сад Марьино. Раннее утро. Туман ещё не рассеялся."
    $ play_narrator("8336d9b0a0201fa8")
    "Павел Петрович стоит с пистолетом в руке — идеальная осанка, холодный взгляд. Базаров напротив, в старом пальто."
    $ play_narrator("7b359f87a3954d7a")
    "Где-то поют птицы, но звук кажется насмешкой."

    show paveldef at right_char
    with dissolve
    show bazarovdef at left_char
    with dissolve

    voice "voice/pavel/703a3985bb904b63.mp3"
    pavel "{i}(холодно){/i} С теоретической точки зрения дуэль — нелепость; ну, а с практической… мы с вами будем стреляться."

    voice "voice/bazarov/750b67c7557885d9.mp3"
    bazarov "Вы вполне оправдываете моё мнение."

    voice "voice/pavel/48b1ad289a3b8609.mp3"
    pavel "Я хочу, чтобы вы поняли: я не потерплю вашего присутствия здесь после того, что произошло."

    voice "voice/bazarov/88931af944bd6d1b.mp3"
    bazarov "Я не собираюсь оставаться. Но если вы настаиваете… давайте покончим с этим."

    $ play_narrator("1b48e563f94cb0c3")
    "Секунданты отводят три шага. Листья лежат на траве и не шевелятся."

    menu:
        "Крикнуть: «Стрелять в воздух!» — и встать между ними":
            $ mercy += 2
            "{i}(Аркадий бросается вперёд, между дулами, и в этот момент кто-то даёт промах, а кто-то — нет.){/i}"
            play sound "sounds/the-dry-cry-of-a-raven-and-incomprehensible-exclamations.ogg"
            $ play_narrator("1452c85038120e61")
            "Грохот. Дым. Павел Петрович пошатывается и медленно опускается на траву; пуля задела ногу, ниже колена."
            voice "voice/bazarov/65e7d866ef1f6045.mp3"
            bazarov "{i}(бросает пистолет, бледный){/i} Аркадий! Ты идиот, ты мог попасть под обе. Ну вот, и стреляли из-за твоего великодушия."
            voice "voice/arcardy/2be8a73cdcdc6395.mp3"
            arcardy "{i}(не своим голосом){/i} Ты ранен?"
            voice "voice/bazarov/0a3bc5cf93970f8d.mp3"
            bazarov "Ранен — он. Я не умею попадать в людей, когда они мне не нужны."
        "Не двинуться и смотреть, как всё исполняется по правилам":
            "{i}(Аркадий стоит, засунув руки в карманы, как велено: он учится быть свидетелем.){/i}"
            play sound "sounds/the-dry-cry-of-a-raven-and-incomprehensible-exclamations.ogg"
            $ play_narrator("7e550206aaf12535")
            "Грохот. Павел Петрович пошатывается, потом медленно опускается на траву. Пуля задела ногу."
            voice "voice/bazarov/e2cec01d70175553.mp3"
            bazarov "{i}(не двигаясь){/i} Ваша очередь кончена. Моя — тоже. Можно разойтись и не быть друг другу врагами."
        "Уйти в дом, пока не раздался выстрел":
            $ nihil += 1
            "{i}(Аркадий отворачивается и идёт к дому, быстро, почти бегом.){/i}"
            play sound "sounds/the-dry-cry-of-a-raven-and-incomprehensible-exclamations.ogg"
            $ play_narrator("33497173b4676da8")
            "Выстрел настигает его на полпути, и он останавливается: идти дальше уже нельзя."
            voice "voice/arcardy/0aeaf2aa3d1d3a25.mp3"
            arcardy "{i}(про себя){/i} Я струсил. Я, кажется, впервые в жизни струсил — и не за что себя обвинить, и нечем оправдать."

    $ play_narrator("df1194a8f6911fe0")
    "Базаров бросается к раненому, перевязывает рану. Лицо у него бледное и злое."

    show paveldef at right_char
    with dissolve

    voice "voice/pavel/323a2a4a1d88a129.mp3"
    pavel "{i}(сквозь зубы, но ровно){/i} Дуэль, если вам угодно, не возобновляется. Вы поступили благородно…"

    voice "voice/bazarov/6d13d7cd6ac0b13e.mp3"
    bazarov "{i}(перевязывая, не глядя){/i} Не говорите этого, Павел Петрович. Мне от этого слова тошно."

    voice "voice/pavel/7a4abf79cf12cd3b.mp3"
    pavel "Ваша кровь — на моём жилете. Вы не могли бы быть учтивее, но могли бы быть аккуратнее."

    voice "voice/bazarov/dc354998a597d9e0.mp3"
    bazarov "{i}(усмехается){/i} Я получил по заслугам."

    voice "voice/pavel/00b69698735cab98.mp3"
    pavel "{i}(тихо){/i} Да. Мы оба. Это единственное, в чём мы с вами согласны."

    "{i}(Павла Петровича уносят в дом. Базаров остаётся один на траве и долго смотрит на то место, где стоял противник.){/i}"

    hide bazarovdef
    hide paveldef
    hide arcardiydef
    with dissolve

    $ play_narrator("04351ee16a9bc0c4")
    "Вечером. Приезжает пристав; за ним — слёзы, письма, угрозы участок покинуть. Николай Петрович уговаривает Базарова уехать."

    show nikolaydef at left_char
    with dissolve
    show bazarovdef at right_char
    with dissolve

    voice "voice/nikolay/d8bbb7092dd32bb9.mp3"
    nikolay "Евгений Васильич… ради Бога, уезжайте сегодня. Я вас не виню и не могу вас винить. Но в этом доме вам больше нельзя."

    voice "voice/bazarov/84777f48cb9290c0.mp3"
    bazarov "{i}(встаёт, берёт фуражку){/i} Я не виноват, Николай Петрович. Я здесь был лишний, и это не беда. Вашу Фенечку… вам её не отдать, и я это знаю, и не прошу."

    voice "voice/nikolay/9c331895250b89f1.mp3"
    nikolay "{i}(отводит глаза){/i} Простите меня. За всё."

    voice "voice/bazarov/eeb1ae3d9a7c7b47.mp3"
    bazarov "{i}(уже у двери){/i} Прощайте. Вы единственный честный человек в этой семье — и вам-то и досталось меньше всех."

    stop music fadeout 2.0

    return


# ============================================================
# СЦЕНА 5b. Васильевка (главы XXV–XXVI)
# ============================================================
label scene_5b:

    call chapter_card("ГЛАВА XXV–XXVI", "Васильевка. Дом Базаровых") from _card5c

    scene bazarov_room at bg_kb_slow
    with fade

    play music "music/light-breeze.ogg" fadein 2.0 volume 0.45
    play bgs "music/light-breeze.ogg" volume 0.2

    $ play_narrator("3e025a1dffd91d4b")
    "Небольшой домик в Васильевке. Места вёрст на сорок вокруг — и всё его. Забор, две яблони, баня, колодец с журавлём."
    $ play_narrator("6449273672e93a06")
    "Вечер. Арина Власьевна всё ходит по комнатке и всё переставляет. Василий Иванович в старом сюртуке, с подвязанным платком."

    show vasiliydef at left_char
    with dissolve
    show arinadef at right_char
    with dissolve
    show bazarovdef at center_ghost
    with dissolve

    voice "voice/vasiliy/9e372dadae1afd6d.mp3"
    vasiliy "{i}(кашляет, расшаркивается){/i} Евгений! Сынок! Милости просим, в твоём собственном доме извиняюсь… Арина Власьевна, а? Что ж ты стоишь, подавай!"

    voice "voice/arina/17d39f8ca130c594.mp3"
    arina "{i}(крестится, плачет, смеётся){/i} Женечка… приехал… живой… А мы уж писали, писали — и ни строчки от тебя."

    voice "voice/bazarov/e7e3647db3b18eae.mp3"
    bazarov "{i}(в дверях, устало){/i} Я приехал на три дня. Не больше."

    voice "voice/vasiliy/95e5a4e526d71cca.mp3"
    vasiliy "{i}(садится, не заметив){/i} Три! Это много, это совсем много. Ты кушал, однако? Фомка! Фомка, барин приехал, вынимай…"

    voice "voice/foma/9943545c11c672a4.mp3"
    foma "{i}(басом, обиженно){/i} Да я уж три раза вынимал-с. Я ж не зна, что барин на три дни. Я думал — навек. Нас бы за это и в солдаты. А у вас, барин, на дороге пыль столбом — я думал, вомлидеры едут."

    voice "voice/bazarov/e6887a2e7d62caed.mp3"
    bazarov "{i}(не выдерживает, садится){/i} Вомлидеры — это, брат, хорошо сказано."

    voice "voice/vasiliy/6f5578d366c31513.mp3"
    vasiliy "{i}(оживляясь){/i} Он у меня остряк! А вот, Евгений, я тут книжку сочинил… про… про всё, что я вижу. Ты посмотришь? Ты человек учёный, ты рассуди."

    voice "voice/arina/5814b40e18e52f44.mp3"
    arina "Не трогай его, Вася. Он с дороги."

    voice "voice/vasiliy/fe4cd28c1e643264.mp3"
    vasiliy "{i}(не слушая, достаёт тетрадь, читает нараспев){/i} «О, мой друг, покажи мне путь мой, и да не буду я…»"
    "{i}(Базаров слушает до конца и не перебивает — это в нём новое.){/i}"
    voice "voice/vasiliy/be2389d7eeeb0a80.mp3"
    vasiliy "{i}(взволнованно){/i} Ну? Как? Скажи, сынок, как?"

    menu:
        "Сказать как есть: «Это не годится, батюшка»":
            $ nihil += 1
            $ mercy += 1
            voice "voice/bazarov/9493cefcb5863af5.mp3"
            bazarov "Не годится, батюшка. Это не поэзия, это молитва в рифму. Но ты не бросай писать: мне… приятно, что ты в ней сидишь."
            voice "voice/vasiliy/3c6645408de62072.mp3"
            vasiliy "{i}(всё-таки светится){/i} Приятно! Он сказал: приятно! Арина Власьевна, слыхала? Приятно!"
            voice "voice/arina/bb4b87e16c6e4e47.mp3"
            arina "{i}(крестится){/i} И то ладно. Кушай, Бог с ним с письмом-то."
        "Не читать вслух и отложить тетрадь":
            $ nihil += 1
            voice "voice/bazarov/b09f753a24a36f64.mp3"
            bazarov "{i}(вежливо, холодно){/i} Отложим, батюшка. Я устал, а ты потом всё равно начнёшь сызнова, и мы оба разойдёмся."
            "{i}(Василий Иванович прячет тетрадь, как спрятали бы болезнь, и уходит к окну.){/i}"
            voice "voice/arina/225d9de087759723.mp3"
            arina "{i}(вполголоса){/i} Жаль-то как… Он три года её писал, всё ждал, что ты прочтёшь."
        "Промолчать и обнять отца":
            $ kinship += 2
            $ mercy += 1
            "{i}(Базаров не отвечает. Он встаёт, кладёт руку отцу на плечо и целует его в лысину — один раз, неловко, как человек, который делает это впервые в жизни.){/i}"
            voice "voice/vasiliy/cbb90bd065272443.mp3"
            vasiliy "{i}(замирает, потом хрипло){/i} Арина Власьевна… Арина Власьевна, иди сюда…"
            voice "voice/arina/115c2af20bd06f21.mp3"
            arina "{i}(прижимается к обоим){/i} Господи… Господи… Ну, слава Тебе."
            "{i}(Он не говорит про тетрадь, и они не говорят про тетрадь; и всё-таки это не отрицание — в этом целый дом, побольше любого ответа.){/i}"

    hide bazarovdef
    hide vasiliydef
    hide arinadef
    with dissolve

    $ play_narrator("6462f17b5bc2af90")
    "Ночь. В чулане, где он жил мальчиком, Базаров не спит. За стеной отец и мать шепчутся, чтобы он не услыхал, — и услыхать нельзя только одного: о чём они говорят так тихо."

    show bazarovdef at center_char
    with dissolve

    "{i}(Он достаёт из-под подушки засаленную книжку и откладывает её в сторону; достаёт письмо Аркадия и тоже откладывает; садится и начинает говорить вслух.){/i}"
    voice "voice/bazarov/001f2131f42f9137.mp3"
    bazarov "Никто не заметил. Я приехал — и никто не спросил, для чего. Она не пришла; тот ранен; этот смеётся над Фомкой; а мне некуда девать два месяца."
    "{i}(Пауза.){/i}"
    voice "voice/bazarov/632d07021dc5ed4f.mp3"
    bazarov "Экая скверная штука — всё предвидеть и ничего не хотеть."

    stop bgs fadeout 1.5
    stop music fadeout 1.5

    menu:
        "На другой день написать Аркадию и просить приехать":
            $ kinship += 1
            $ mercy += 1
            show arcardiydef at right_char
            with dissolve
            $ play_narrator("07cc1dd26aa672d8")
            "Через неделю Аркадий в Васильевке. Они ходят по берегу, ловят раков, и Базаров говорит только о науке — как будто лечится."
            voice "voice/bazarov/b9f40f893183ff37.mp3"
            bazarov "{i}(не глядя){/i} Ты заметил: я стал учтив. Это оттого, что мне некуда деть злость. Ты приехал — и у меня её меньше на треть. Пиши чаще."
            voice "voice/arcardy/ff1be2bb0f694375.mp3"
            arcardy "Я приеду ещё. Я, кажется, теперь всегда буду приезжать."
            hide arcardiydef
        "Написать Одинцовой и попросить свидания":
            $ anna_open += 2
            $ play_narrator("cae1d958e02c4cae")
            "Базаров пишет письмо в одну строку и сам относит его на почту. Он не ждёт ответа и получает его раньше, чем ждал кто-нибудь в этом уезде."
            voice "voice/anna/c168d53990b3b33b.mp3"
            anna "{i}(в ответной записке){/i} «Вы были резки; я не умею держать на вас. Но я не умею и не отвечать. Приезжайте; я жду, и мне скучно без вас»."
            voice "voice/bazarov/b5fc39939dd35ed4.mp3"
            bazarov "{i}(читает дважды и смеётся; смех выходит не весёлый){/i} «Мне скучно без вас». Это, брат, уже не спокойствие. Это, брат, обещание."
        "Не писать никому":
            $ nihil += 1
            $ play_narrator("d3d819382cb54e3b")
            "Проходят три недели. Базаров ездит по уезду по мелким нуждам, лечит за гроши, дерёт с мужиками коросту; у него вырывают зуб у помещика, вправляют руку солдату и зовут его «чёрт». Он не пишет ни слова."
        "Договорить слово о сене — и не подать руки":
            $ hay_branch = True
            jump scene_5b_hay

    label story_after_hay:

    # возврат из новой ветки: чулан Василиевки, тот же поздний час
    scene bazarov_room at bg_kb
    with dissolve

    hide bazarovdef

    $ play_narrator("d6194e4f2b109f16")
    "Осенью приносят известие: в соседней деревне померли от скорбного тифа, и фельдшер прислал записку — пусть кто-нибудь приедет вскрыть."

    show bazarovdef at left_char
    with dissolve
    show vasiliydef at right_char
    with dissolve

    voice "voice/bazarov/875e56a7e7ec5bf5.mp3"
    bazarov "{i}(берёт шляпу){/i} Поеду, батюшка. Фельдшер один не справится, а тиф у вас по уезду ходит."

    voice "voice/vasiliy/53f9947736ae9597.mp3"
    vasiliy "{i}(встаёт, придерживаясь за стол){/i} Да ты, Женечка, к нам ещё не обвыкся. Подожди недельку…"

    voice "voice/bazarov/02cb8bc584ec2ac2.mp3"
    bazarov "Недельку. Да. С этой болезнью всегда ждут недельку, а потом хоронят."

    "{i}(Он возвращается поздно, с порезом на пальце. Перевязывает сам, не показывая матерям, и в ту же ночь у него начинает ломить спину.){/i}"

    hide bazarovdef
    hide vasiliydef
    with dissolve

    stop music fadeout 2.0

    jump scene_6


# ============================================================
# НОВАЯ ВЕТКА A. ГЛАВА X — «песенка спета» (сцена у беседки)
# ============================================================
label scene_4_speta:

    call chapter_card("ГЛАВА X · ВЕТВЬ", "Беседка в Марьине") from _cardA

    scene maryino_morning at bg_kb
    with fade

    play music "music/light-breeze.ogg" fadein 1.5 volume 0.5

    $ play_narrator("dcace01f43bc98b7")
    "Возвратимся на два дня назад, в аллее Марьина, где у беседки не могут видеть говорящих."

    $ play_narrator("5105f70098c38c0a")
    "Твой отец добрый малый, — говорил Базаров, — но он человек отставной, его песенка спета."

    $ play_narrator("6716e1f8cee7100a")
    "Третьего дня, я смотрю, он Пушкина читает, — продолжал Базаров. — Растолкуй ему, пожалуйста, что это никуда не годится. Пора бросить эту ерунду."

    $ play_narrator("5148e99f3a10c0a1")
    "Что бы ему дать? — спросил Аркадий. — Да, я думаю, Бюхнерово Stoff und Kraft на первый случай."

    $ play_narrator("0125d014ab385f43")
    "Я сам так думаю, — заметил Аркадий. — Stoff und Kraft написано популярным языком."

    $ play_narrator("d9d681cf62dbd43f")
    "А в гостиной, у окна, Николай Петрович сидел с книгой в руках и не читал — он слушал, как за стеной решают его дело."

    $ play_narrator("dba26ccbcc915b58")
    "Либо я глуп, либо это всё — вздор, — проговорил он вполголоса, откладывая брошюру. — Должно быть, я глуп."

    $ play_narrator("a1cc859ca7f94830")
    "В тот же вечер Базаров сказал Аркадию: Рафаэль гроша медного не стоит; и прибавил: или всё, или ничего."

    $ play_narrator("af06ad92cbfb2f3e")
    "Аркадий не спорил. Он подумал: либо я глуп, либо это всё — вздор; и вышло, что он согласился."

    $ play_narrator("e186eb1b1054d818")
    "Так, — говорил Базаров, — вот как должны современные молодые люди выражаться. Прежде они просто были болваны, а теперь скажут: всё на свете вздор — и дело в шляпе."

    $ play_narrator("9ab15eb565d38f2b")
    "Стань моим учеником, — прибавил он. — Езжай ко мне на квартирку; я буду тебя читать лекции. Мы с тобой составим пару."

    $ play_narrator("fcb691548e5fe32b")
    "Аркадий первый раз в жизни согласился без спора — и ему показалось, что земля ушла из-под ног не у отца, а у него самого."

    $ play_narrator("bda5f6278719bce7")
    "На другой день он произносил у самовара первую свою отрицательную речь — про отрицание всё, и искусства, и поэзии, и страшно вымолвить."

    $ play_narrator("f3bc681eff4ee241")
    "Сказав, он вышел на воздух и постоял в аллее, как человек, который проиграл что-то, чего не умел назвать."

    menu:
        "Сказать отцу Базарова вслух: «Он не глуп, батюшка»":
            $ speta_branch = True
            $ play_narrator("ac962aa7fd8a2198")
            "Николай Петрович, — сказал Аркадий, входя в гостиную, — вы не глуп; а это всё — вздор только наполовину. Другую половину мы у вас отнимем — и, чую, не отдам."

            $ play_narrator("d22748b9de37ae83")
            "Старик вспыхнул, как в тот час, когда его сын целовал его в плечо, и ничего не ответил; только на столе остался лежать том Пушкина — не унесённый."

            $ play_narrator("d5539c3ae96c63f8")
            "Базаров, узнав про то, рассмеялся и сказал: нет, брат, ты не годишься в ученики; тебя делать надо, как тесто — в теплое место."

            jump story_after_sitnikov
        "Промолчать — и сесть рядом с отцом в беседке":
            $ play_narrator("0fa034d84e6fb431")
            "Он не сказал ничего и сел рядом; они молчали оба, как молчали когда-то на террасе, и молчание это было не уступкой, а отцовством."

            $ play_narrator("171cadabfc778eee")
            "Песенка, однако, не была спета: её просто никто не дослушал."

            jump story_after_sitnikov


# ============================================================
# НОВАЯ ВЕТКА B. ГЛАВА XXI — сено и «отрезанный ломоть»
# ============================================================
label scene_5b_hay:

    call chapter_card("ГЛАВА XXI · ВЕТВЬ", "Стог сена в Васильевке") from _cardB

    scene nikolskoe at bg_kb
    with fade

    play bgs "music/light-breeze.ogg" volume 0.2

    $ play_narrator("bbcdd88aa44999be")
    "Настал полдень. Солнце жгло из-за тонкой завесы сплошных беловатых облаков; одни петухи задорно перекликались на деревне."

    $ play_narrator("a6cbe6a063c353cf")
    "Аркадий и Базаров лежали в тени небольшого стога сена, подостлавши под себя охапки две шумливо-сухой, но еще зеленой и душистой травы."

    $ play_narrator("f4217be29edb611f")
    "Та осина, — заговорил Базаров, — напоминает мне мое детство; я никогда не скучал возле них. Не понимал тогда, что не скучал оттого, что был ребенком. Ну, теперь я взрослый, талисман не действует."

    $ play_narrator("dbbabfff88c32735")
    "Я думаю: хорошо моим родителям жить на свете! а я… я чувствую только скуку да злость."

    $ play_narrator("71f91181ed441e65")
    "Узенькое местечко, которое я занимаю, до того крохотно в сравнении с остальным пространством, где меня нет и где дела до меня нет."

    $ play_narrator("86c0226fb523a689")
    "Вот, сказал ты, Россия тогда достигнет совершенства, когда у последнего мужика будет такое же помещение… А я и возненавидел этого последнего мужика, Филиппа или Сидора, для которого я должен из кожи лезть и который мне даже спасибо не скажет."

    $ play_narrator("ba76162572ea4f2b")
    "Принципов вообще нет — а есть ощущения. Все от них зависит. Я придерживаюсь отрицательного направления — в силу ощущения."

    $ play_narrator("06035f5cd75d08d0")
    "Настоящий человек тот, о котором думать нечего, а которого надобно слушаться или ненавидеть."

    $ play_narrator("c22de55906b13d4e")
    "Нет, брат! Решился все косить — валяй и себя по ногам!"

    $ play_narrator("f179858bfbc284c1")
    "Природа навевает молчание сна, — сказал Пушкин, — произнес Базаров. — Никогда он ничего подобного не сказал, — промолвил Аркадий."

    $ play_narrator("de31207dea409063")
    "Кстати, он, должно быть, в военной службе служил. — Пушкин никогда не был военным! — Помилуй, у него на каждой странице: на бой, на бой! за честь России!"

    $ play_narrator("8c31cb7b2fa21120")
    "Оба приятеля полежали некоторое время в молчании; какое-то почти враждебное чувство охватывало сердца обоих молодых людей."

    $ play_narrator("39b547bc36dedffd")
    "Ах, Аркадий! сделай одолжение, поссоримся раз хорошенько — до положения раз, до истребления. Здесь, на сене, вдали от света и людских взоров — ничего."

    $ play_narrator("3b9c8dd2f2a92519")
    "Базаров растопырил свои длинные и жесткие пальцы… Аркадий почувствовал невольную робость."

    $ play_narrator("258b93a219c6527a")
    "А! вот вы куда забрались! — раздался голос Василия Ивановича. — Я гляжу в небо только тогда, когда хочу чихнуть, — проворчал Базаров и прибавил вполголоса: жаль, что помешал."

    $ play_narrator("d2fc4d9c4378b548")
    "Но никакая дружба долго не выдержит таких столкновений."

    menu:
        "Сказать слово о сене и подать руку — как в тот день":
            $ play_narrator("ea9c13dd259e7bf6")
            "Ну, полно, — шепнул Аркадий и пожал украдкой своему другу руку."

            jump story_after_hay
        "Промолчать и не подать руки":
            $ play_narrator("2c8289737f160f2e")
            "Аркадий не сказал ничего и не подал руки; Василий Иванович звал их обедать, и они пошли за ним, не идя больше никогда вместе."

            jump ending_loмоть


# ============================================================
# НОВАЯ ВЕТКА C. ГЛАВА XXV — Катя в саду Никольского
# ============================================================
label scene_7_katya:

    call chapter_card("ГЛАВА XXV · ВЕТВЬ", "Сад в Никольском") from _cardC

    scene nikolskoe at bg_kb
    with fade

    play music "music/light-breeze.ogg" fadein 2.0 volume 0.45

    $ play_narrator("df0d02742967d882")
    "В Никольском, в саду, в тени высокого ясеня, сидели на дерновой скамейке Катя с Аркадием; на земле возле них поместилась Фифи."

    $ play_narrator("0772a1de7f3af2b1")
    "Они молчали оба; но именно в том, как они молчали, сказывалось доверчивое сближение."

    $ play_narrator("a362cedecfe0acc1")
    "Я не люблю Гейне, — заговорила Катя, — ни когда он смеется, ни когда он плачет; я его люблю, когда он задумчив и грустит. — А мне нравится, когда он смеется, — заметил Аркадий."

    $ play_narrator("e3cf7903af6ec6dc")
    "Вот эта не упрекает меня за то, что я красиво выражаюсь, — подумал Аркадий, и ему стало и стыдно и хорошо."

    $ play_narrator("679e54e0bdedda9e")
    "Знаете ли что, Катерина Сергеевна? — сказал он. — Он хищный, а мы с вами ручные. — И я ручной? — Катя кивнула головой."

    $ play_narrator("1a340ea54da90417")
    "Послушайте, ведь это, в сущности, обидно. — Разве вы хотели бы быть хищным? — Хищным нет, но сильным, энергическим. — Этого нельзя хотеть… Вот ваш приятель этого и не хочет, а в нем это есть."

    $ play_narrator("a2d2c8973f7857e3")
    "Я готова покоряться, только неравенство тяжело. А уважать себя и покоряться — это я понимаю; это счастье; но подчиненное существование… Нет, довольно и так."

    $ play_narrator("378441d3e553c356")
    "Довольно и так, — повторил за Катей Аркадий; и в тот час, когда слово уже сидело на языке, он услыхал в памяти: об одном прошу тебя — не говори красиво."

    $ play_narrator("d8166d062f1c878d")
    "Он встал, не сказав ничего, и пошёл по коридору к себе в комнату."

    $ play_narrator("6207f2f39446f13a")
    "Катя уронила обе руки вместе с корзинкой на колени и долго смотрела вслед Аркадию; губы не улыбались, и темные глаза выражали недоумение и какое-то другое, пока еще безымянное чувство."

    $ play_narrator("1d7fcc4234ee8fa8")
    "Ты одна? — раздался голос Анны Сергеевны. — Кажется, ты пошла в сад с Аркадием. — Я одна, — не спеша промолвила Катя."

    $ play_narrator("5406dc402f164145")
    "Дворецкий нагнал Аркадия в коридоре и доложил, что у него сидит господин Базаров. — Евгений! — пробормотал почти с испугом Аркадий."

    menu:
        "Вернуться в сад и сказать: «ни на кого в свете не променяю»":
            $ play_narrator("b8ce73c7bf942687")
            "Катерина Сергеевна! — заговорил вдруг Аркадий. — Знайте, что я вас не только на вашу сестру, — ни на кого в свете не променяю."

            $ play_narrator("1b5cac8c64023026")
            "Неделю тому назад, в небольшой приходской церкви, тихо и почти без свидетелей состоялись две свадьбы: Аркадия с Катей и Николая Петровича с Фенечкой."

            $ play_narrator("c0f534671663ed67")
            "В память Базарова, — шепнула Катя на ухо своему мужу и чокнулась с ним. Аркадий в ответ пожал ей крепко руку, но не решился громко предложить этот тост."

            jump story_after_wedding
        "Уехать к себе и не вернуться в сад":
            $ play_narrator("6ab59b6c14bae554")
            "Он не повернул назад; на другой день Базаров уехал, и дороги их разошлись так, как расходятся в поле две тропинки после дождя."

            jump ending_molchanie


# ============================================================
# РАЗВЯЗКА 4. Песенка спета (ветка А)
# ============================================================
label ending_speta:

    scene black
    with fade

    play music "music/waiting_theme.ogg" fadein 2.0 volume 0.35

    $ play_narrator("92da8965f06ff05e")
    "Прошло полгода. Базаров не видал Аркадия в Марьине с осени и не ждал; но в Петербурге, в корчме, у полуоткрытого окна, сидел молодой человек в клетчатом пальто и повторял слова о том, что принципов нет, а есть ощущения."

    $ play_narrator("6adb33a7e53ac1cc")
    "Езжай ко мне на квартирку; я буду тебя читать лекции, — твердил он про себя и каждую неделю ездил; и прежде, бывало, он спорил и оставался побежден, а теперь не спорил и оставался пуст."

    $ play_narrator("f9f33a8ffe9dea5d")
    "Мы ломаем, потому что мы сила, — говорил он в гостиных, выпрямляясь; и никто не спорил, и никому не было дела."

    $ play_narrator("89e6440d192934d4")
    "После смерти Базарова — его не стало той же осенью, в Васильевке, от тифа, вскрытого им трупа — Ситников и Козьин тотчас стали говорить о деле Базарова в двух темных журнальцах."

    $ play_narrator("b0717b6d65ef7c7d")
    "Через два года к ним причислили и Аркадия Николаича: он печатался под тремя подписями и называл это иронией; отец же его по-прежнему мыкался по участку в мировых посредниках."

    $ play_narrator("c3f908b18e5231e6")
    "Николай Петрович жил в Марьине, запершись в своей комнате с книгами, которых не раскрывал, и только по воскресеньям произносил длинные речи о манципации — и для образованных, и для необразованных."

    $ play_narrator("1f9d2346e75cf4b9")
    "Павел Петрович жил в Дрездене, у серебряной пепельницы в виде мужицкого лаптя; он ничего русского не читал и всё делал добро, сколько мог."

    $ play_narrator("4b2aa86e4b381314")
    "Аркадий приехал на сельское кладбище один, в ноябре, и постоял у железной ограды, где две молодые елки были посажены по обоим концам."

    $ play_narrator("b43e599c3ec28bac")
    "Как почти все наши кладбища, оно явило вид печальный: окружавшие его канавы давно заросли; овцы безвозбранно бродили по могилам."

    $ play_narrator("2bbfb08a3722036b")
    "Неужели их молитвы, их слезы бесплодны? Неужели любовь, святая, преданная любовь не всесильна? — спрашивали над могилой цветы; и никто не ответил."

    $ play_narrator("87c01d458f148dea")
    "Они говорят также о вечном примирении и о жизни бесконечной, — дописал бы Тургенев, если бы эта рукопись осталась у него в руках."

    jump finale_card


# ============================================================
# РАЗВЯЗКА 5. Отрезанный ломоть (ветка B)
# ============================================================
label ending_loмоть:

    scene bazarov_room at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 2.5 volume 0.3

    $ play_narrator("39456dd80dad33d4")
    "Базаров уехал на другой день. Вели-ка завтра наших лошадей к Федоту выслать на подставу, — сказал он отцу с натянутым зевком, и Василий Иванович вынул платок и, сморкаясь, наклонился чуть не до земли."

    $ play_narrator("c7151342590c9898")
    "Бросил, бросил нас, — залепетал он, — бросил; скучно ему стало с нами. Один как перст теперь, один! — повторил он несколько раз и каждый раз выносил вперед свою руку с отделенным указательным пальцем."

    $ play_narrator("8e9d9088df84b0da")
    "Что делать, Вася! Сын — отрезанный ломоть. Он что сокол: захотел — прилетел, захотел — улетел; а мы с тобой, как опенки на дупле, сидим рядком и ни с места."

    $ play_narrator("3b22183e8cce4e4b")
    "Василий Иванович пожалел свою старушку; он не захотел сказать ей на ночь, какое горе ее ожидало."

    $ play_narrator("e17c917e2c118127")
    "Прошло полгода; Базаров не вернулся ни через месяц, как обещал, и работа разлучила их окончательно."

    $ play_narrator("dc25fc65267dc002")
    "Осенью приносят известие о мёртвых от тифа в соседней деревне; и он едет — и красная точка на пальце делает свое дело."

    $ play_narrator("0b3683928e7566d9")
    "Лихорадка прошла шесть дней; он лежал бледный, потный, глаза горели лихорадкой; он помнил про последнюю сцену на сене и не позвал."

    $ play_narrator("c150cc98788fa7f3")
    "Перед концом он сказал отцу: бросил, бросил вас, — и это было единственное его покаяние; он не умел его повторить."

    $ play_narrator("95da04e4e8067f15")
    "Аркадий получил письмо с печатью и не написал ответа — не от гордости; ему нечего было сказать."

    $ play_narrator("6ff15bc185dfd64b")
    "Двенадцать лет спустя Аркадий приехал в Васильевку; дом был маленький, тоже как будто внезапно съежившийся и подряхлевший; Тимофеич его не сразу признал."

    $ play_narrator("5c445f75eb5d8a8a")
    "Есть небольшое сельское кладбище в одном из отдаленных уголков России; между могилами есть одна, до которой не касается человек: две молодые елки посажены по обоим ее концам."

    $ play_narrator("a7bb84949be67750")
    "Он простоял у ограды до вечера и не молился — не оттого, что не захотел, а оттого, что разучился."

    jump finale_card


# ============================================================
# РАЗВЯЗКА 6. Безымянное чувство (ветка C)
# ============================================================
label ending_molchanie:

    scene nikolskoe at bg_kb_slow
    with fade

    play music "music/light-breeze.ogg" fadein 2.0 volume 0.4

    $ play_narrator("dab7ac3d2dff4e26")
    "Прошло шесть месяцев. В небольшой приходской церкви, тихо и почти без свидетелей, состоялись две свадьбы, но не те, которых ждали в Никольском."

    $ play_narrator("dfdbee256c18fb51")
    "Катерина Сергеевна вышла замуж не по любви, но по убеждению, за человека очень умного, законника, с крепким практическим смыслом, твердою волей, — доброго и холодного как лед."

    $ play_narrator("de520eb92c022690")
    "Кирсановы, отец с сыном, поселились в Марьине. Аркадий сделался рьяным хозяином, и ферма уже приносит довольно значительный доход; Николай Петрович попал в мировые посредники и произносит длинные речи."

    $ play_narrator("6740bfe12013a0b0")
    "Аркадий Николаевич не женился и был самым теплым человеком в двух домах; маленьким Колей он любовался молча."

    $ play_narrator("e81189782057af03")
    "В память Базарова, — шепнула Катерина Сергеевна на ухо мужу, когда пришла пора чокаться; Аркадий поднял свой бокал через весь стол, не расслышав."

    $ play_narrator("0fce187dddd79830")
    "Железная ограда вокруг могилы окружала её; две молодые елки были посажены по обоим ее концам; к ней часто приходили два уже дряхлые старичка и, поддерживая друг друга, становились на колени."

    $ play_narrator("a2a68af5d4bb6fd7")
    "Цветы, растущие на ней, безмятежно глядят на нас своими невинными глазами: они говорят о вечном примирении и о жизни бесконечной."

    $ play_narrator("d9096f7f0c35be73")
    "Одно лишь слово так и осталось несказанным — и лежало между ними, как лежит на дне реки то, что не выловишь."

    jump finale_card


# ============================================================
# СЦЕНА 6. Смерть Базарова (главы XXVII–XXVIII)
# ============================================================
label scene_6:

    call chapter_card("ГЛАВА XXVII", "Скорбный тиф") from _card6

    scene bazarov_room at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 2.0 volume 0.4
    play bgs "music/light-breeze.ogg" volume 0.15

    $ play_narrator("0517dce3840377f4")
    "Маленький домик родителей Базарова. Тёмная комната, тяжёлый воздух."
    $ play_narrator("c43f1b69e9b756b4")
    "Базаров лежит на кровати — бледный, потный, глаза горят лихорадкой. За окном — тихий дождь."
    $ play_narrator("6042c63945b6861c")
    "Он заразился тифом, вскрывая труп крестьянина. Прошло шесть дней с того вечера, когда он показал матери красную точку царапины на пальце."

    "{i}(Приезжий доктор из города осмотрел его четверть часа назад и теперь ходит у окна, подбирая слово.){/i}"
    voice "voice/doct/01b7d6e0cc990818.mp3"
    doct "Вам, может быть, легче через неделю. Мы… примем всё, что возможно. Я пришлю человека завтра."

    voice "voice/bazarov/b3fb9b8d40b9ce54.mp3"
    bazarov "{i}(хрипло){/i} Не трудитесь. Я знаю, что это за болезнь, и знаю, чем она кончается. Мне не о чем с вами толковать; лучше скажите им."

    "{i}(Доктор уходит. Дверь отворяется снова.){/i}"

    voice "voice/vasiliy/acbdbc5a3053991e.mp3"
    vasiliy "{i}(в комнату, на бегу){/i} Евгений! Сынок! Анна Сергеевна Одинцова здесь… и привезла сего господина доктора!"

    show bazarovdef at center_char
    with dissolve

    voice "voice/bazarov/a51030e809a43389.mp3"
    bazarov "{i}(с трудом открывает глаза){/i} Что ты сказал?.. Анна Сергеевна Одинцова… Здесь?"

    hide bazarovdef
    show annadef at right_char
    with dissolve
    show bazarovdef at left_char
    with dissolve

    "{i}(Одинцова подходит тихо.){/i}"
    voice "voice/anna/65505beefea83b11.mp3"
    anna "Евгений Васильевич… Я приехала."

    voice "voice/bazarov/c0dbb63fb4d48d2b.mp3"
    bazarov "{i}(слабая улыбка){/i} Вот как… Вы всё-таки приехали… Спасибо… Я знал, что вы не забудете… Хотя и говорил, что всё это вздор…"

    voice "voice/anna/3ed4c53c0aea9f04.mp3"
    anna "{i}(спокойно, но с дрожью в голосе){/i} Вы говорили, что не хотели бы, чтобы я приезжала… Но я всё равно приехала."

    menu:
        "Сказать ей всё, что не сказал в Никольском":
            $ anna_open += 2
            $ bazarov_spoke_all = True
            voice "voice/bazarov/5b75cf46b06cc126.mp3"
            bazarov "{i}(тяжело дыша){/i} Я вас любил. Не умно, не красиво… как собака. Я думал, это пройдёт, как проходит у людей всё, что они называют болезнью."
            voice "voice/anna/7af7ffae3a94d4e1.mp3"
            anna "{i}(наклоняется ниже){/i} Не проходило?"
            voice "voice/bazarov/6263b7ad55a91671.mp3"
            bazarov "Нет. Я приехал сюда умирать и всё-таки ждал, что вы придёте. Не потому, что поверил, — а потому, что нечего больше ждать."
            voice "voice/anna/19fbad27fd823442.mp3"
            anna "{i}(голос рвётся впервые){/i} Простите меня. Я хотела спокойствия. Я его дождалась… и вот я здесь."
            voice "voice/bazarov/5d97ab785cf3e568.mp3"
            bazarov "Не просите прощения. Это единственное, чего я у вас не возьму. Скажите лучше, что вам тоже было не по себе в Никольском."
            voice "voice/anna/e811f22abdfd3437.mp3"
            anna "{i}(долго молчит){/i} Был вечер, когда я послала за вами. Я тогда не знала, что это значит. Теперь знаю."
        "Не говорить о любви и спросить про дорогу":
            voice "voice/bazarov/e8d1a91afc3571be.mp3"
            bazarov "{i}(отворачиваясь к стене){/i} Вы изволили приехать верхом? Дорога распухла. Это не стоит того… ничего не стоит. Посидите и уходите, Анна Сергеевна. Мне тяжело быть благодарным."
            voice "voice/anna/6218c9b7cd793480.mp3"
            anna "{i}(не двигается){/i} Я не уйду, пока вы не взглянете на меня."
            voice "voice/bazarov/36f29cc3caf6a94c.mp3"
            bazarov "{i}(с усилием, через силу){/i} Вы были единственная женщина, которая могла мне пригодиться… и я из этого ничего не сделал. А жаль. Ах, как жаль!"
            "{i}(Он всё-таки поворачивает голову — и она видит, что он плачет без слёз.){/i}"
            $ mercy += 1

    hide annadef

    $ play_narrator("7f0aab06d06dc3b3")
    "Арина Власьевна входит с компрессом и не выходит из комнаты больше ни разу за весь день."

    show vasiliydef at left_char
    with dissolve
    show arinadef at right_char
    with dissolve
    show bazarovdef at center_ghost
    with dissolve

    "{i}(Базаров долго молчит, потом начинает говорить — тихо, но твёрдо.){/i}"
    voice "voice/bazarov/8e55aaa22d9b3fd0.mp3"
    bazarov "Отец… мать… не плачьте… Это глупо… Жизнь — пустая штука… Я скоро вас избавлю…"

    voice "voice/vasiliy/b0739f4b7b61c0df.mp3"
    vasiliy "{i}(плачет){/i} Евгений… сынок… как же так… ты же доктор… ты должен был жить…"

    voice "voice/bazarov/81024aeb7039b8b8.mp3"
    bazarov "{i}(усмехается слабо){/i} Доктор… который сам умирает от тифа… Ирония судьбы, правда?"

    voice "voice/arina/1670abdab90dfe4b.mp3"
    arina "{i}(рыдая){/i} Женечка… милый мой…"

    voice "voice/bazarov/f5290b2416d80563.mp3"
    bazarov "Матушка. Мне нужно тебя попросить. Позови… нет, не надо. Оставь."
    "{i}(Он думает.){/i}"
    voice "voice/bazarov/ea51671dfbbf8b63.mp3"
    bazarov "Одно скажи: я вас любил. Только не говори им, что я плакал. Я не хочу, чтобы про меня говорили: он был сентиментален."

    menu:
        "Попросить отца позвать священника — и выговорить вслух своё имя":
            $ mercy += 2
            $ saw_last_hours = True
            voice "voice/bazarov/7d2a055a60a4d041.mp3"
            bazarov "{i}(тихо){/i} Батюшка. Позови… позови священника. Не затем, чтобы я поверил, а чтобы ты поверил. И скажи ему, как меня звать, а то я сам не смогу."
            voice "voice/vasiliy/06fd94432dc583b6.mp3"
            vasiliy "{i}(вскакивает, кидается к дверям, оборачивается){/i} Жив! Он живой! Арина Власьевна, он живой, он просит!"
            "{i}(Арина Власьевна начинает молиться вслух, нараспев, как молилась в поле, — и Базаров слушает до конца.){/i}"
            voice "voice/bazarov/f1cf5e6671910981.mp3"
            bazarov "{i}(еле слышно){/i} Красиво, однако… Не умно — а красиво. Вот видишь, батюшка: я всё-таки не всё отверг."
        "Никого не звать и попросить, чтобы вышли все":
            $ nihil += 1
            voice "voice/bazarov/4d7ed5041a1521e9.mp3"
            bazarov "Никого не зовите. Я хочу умереть один, как я жил: без церемоний. Оставьте дверь открытой, чтобы меня не тошнило от духоты."
            "{i}(Родители выходят, не шумя, как выходят из церкви. В комнате остаются окно, дождь и человек, который всё просчитал — и не просчитал только этого.){/i}"
            voice "voice/bazarov/4a3481789c4846de.mp3"
            bazarov "{i}(через час, сам, вполголоса, в пустоту){/i} Барон… это я так, для упражнения мускулов… Не надо. Никого не надо. Никому."
        "Позвать Аркадия и говорить с ним как с равным":
            $ saw_last_hours = True
            $ kinship += 1
            $ mercy += 1
            show arcardiydef at side_right_char
            with dissolve
            "{i}(Аркадий приезжает на рассвете. Он не говорит ни слова и садится на пол у кровати.){/i}"
            voice "voice/arcardy/6071ade3a88282de.mp3"
            arcardy "Я здесь."
            voice "voice/bazarov/c47a954e5d36dcaa.mp3"
            bazarov "{i}(не открывая глаз){/i} Это хорошо. Ты… единственный… кого я не стыжусь. Скажи отцу, что я его… ну, ты сам скажи, ты лучше меня умеешь."
            voice "voice/arcardy/92e7d5c91acdb82c.mp3"
            arcardy "{i}(сквозь зубы){/i} Я не умею, Евгений. Научи."
            voice "voice/bazarov/42e209ec20618bda.mp3"
            bazarov "Нечему учить. Живи. Это не моя наука, а твоя. Ты — не я, ты теплее, и в том твоя польза… Аркаша… подай воды…"

    hide arcardiydef
    hide arinadef
    hide vasiliydef

    "{i}(Базаров закрывает глаза. Дождь кончается. Василий Иванович выходит на крыльцо и долго не может заговорить.){/i}"

    voice "voice/vasiliy/3874d5ac1a09c9e0.mp3"
    vasiliy "{i}(никому){/i} Кончился… Мой… свет… кончился."

    hide bazarovdef
    with dissolve

    $ play_narrator("9623a374c6b45e70")
    "Прошло три дня."

    stop bgs fadeout 2.0
    stop music fadeout 3.0

    call scene_6b from _funeral

    jump scene_7


# ============================================================
# СЦЕНА 6b. Похороны
# ============================================================
label scene_6b:

    call chapter_card("ГЛАВА XXVIII", "Похороны") from _card6b

    scene cemetery at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 2.0 volume 0.3
    play sound "sounds/the-dry-cry-of-a-raven-and-incomprehensible-exclamations.ogg"

    $ play_narrator("6cb2c60ae9f0f127")
    "Дождь. Небольшое сельское кладбище у подошвы горы, между двумя вековыми елями, — как он сам велел."
    $ play_narrator("04a59c8800e3629d")
    "Певчих мало: за гробом идут три человека да солдат, который служил в барской избе. Могила старая, заброшенная; камня на плиту не нашлось."

    show arinadef at left_char
    with dissolve
    show vasiliydef at right_char
    with dissolve

    voice "voice/arina/1a20bfd8c7d0a779.mp3"
    arina "{i}(не рыдая, ровно){/i} Вася. Он сказал: чтобы не плакали. А я не могу не плакать, значит, я не слушаюсь. Значит, он не велел. Значит, он жив."

    voice "voice/vasiliy/4452553abced4759.mp3"
    vasiliy "{i}(кладёт землю руками){/i} Жив. Пока ты это выговариваешь — жив. А после… после я буду приходить сюда каждый день и говорить с ним, и он не ответит, и это будет ответ."

    if saw_last_hours:
        "{i}(В конце процессии стоит Аркадий. Он держит в руке цветы, которые не успел положить вовремя, и кладёт их молча.){/i}"
    else:
        "{i}(В конце процессии стоит Аркадий, один, без Кати; и чуть в стороне, в тёмной шляпе, — женщина, которая не подошла к могиле и уехала, не назвавшись.){/i}"

    hide arinadef
    hide vasiliydef
    with dissolve

    $ play_narrator("56a434c95d4a96af")
    "Две недели спустя Арина Власьевна начинает носить ему обед на кладбище и ставить его на могиле; Василий Иванович не мешает ей, а сам после этого долго сидит у окна с незажжённой трубкой."

    stop music fadeout 2.5

    return


# ============================================================
# СЦЕНА 7. Свадьбы (эпилог, часть 1)
# ============================================================
label scene_7:

    call chapter_card("ЭПИЛОГ · 1", "Свадьбы") from _card7

    scene church_wedding at bg_kb
    with fade

    play music "music/light-breeze.ogg" fadein 2.0 volume 0.7

    $ play_narrator("50ffd86797fc5638")
    "Церковь в Марьино. Яркий солнечный день. Звенят колокола."
    $ play_narrator("6efaa07805ccb5d6")
    "Аркадий в новом фраке держит руку Кати. Рядом — Николай Петрович и Фенечка, оба сияют тихим счастьем. Павел Петрович стоит в стороне, улыбаясь."

    show arcardiydef at left_char
    with dissolve
    show catyadef at right_char
    with dissolve

    voice "voice/arcardy/5adb83f52e9bd270.mp3"
    arcardy "{i}(держа Катю за руку){/i} Катерина Сергеевна… я люблю вас навек и безвозвратно… Вы для меня всё. Я не могу представить жизнь без вас."

    voice "voice/catya/de5269f5c0d782c0.mp3"
    catya "{i}(тихо, улыбаясь){/i} Да… Я тоже."

    voice "voice/catya/c14ffc0388d0e5d0.mp3"
    catya "Только ты не меняйся, Аркадий. Я тебя полюбила таким, каким ты пришёл в Никольское с Базаровым, а не таким, каким ты стал после."

    voice "voice/arcardy/577a82762cad4458.mp3"
    arcardy "{i}(серьёзно){/i} Тогда я останусь тем, другим. Обещать я не умею, а это могу."

    hide arcardiydef
    hide catyadef

    show nikolaydef at left_char
    with dissolve
    show fedosiyadef at right_char
    with dissolve

    "{i}(Николай Петрович тихо говорит Фенечке во время церемонии.){/i}"
    voice "voice/nikolay/5b5853c569b477d4.mp3"
    nikolay "Теперь всё будет по-другому… Мы поженимся тихо, без шума. Ты не против?"

    voice "voice/fedosiya/73af2882d3024f69.mp3"
    fedosiya "{i}(краснея){/i} Конечно, нет…"

    voice "voice/fedosiya/60ca720f7b6d1463.mp3"
    fedosiya "А Митя тебя папой зовёт. Он вас, Николай Петрович, всё ждал, а я всё боялась."

    voice "voice/nikolay/8d215228d2b225ed.mp3"
    nikolay "{i}(оборачивается к алтарю){/i} Я ждал дольше его. Мне-то бояться было нечего — мне только стыдно было, а стыд не беда."

    hide nikolaydef
    hide fedosiyadef

    $ play_narrator("7d322c760bcfd2f7")
    "За оградой церкви Ситников — уже женатый на Курлесевой и печатающий в журнале — разглагольствует о правах женщины; Лиза выходит замуж за мелкого поэта; никто из них не вспоминает Базарова, кроме Кати, которая однажды переспросила: «А где же Евгений Васильевич?»"

    show paveldef at left_char
    with dissolve
    show arcardiydef at right_char
    with dissolve

    voice "voice/pavel/a42c9f1288ff28cb.mp3"
    pavel "{i}(после церемонии){/i} Поздравляю, племянник. Ты сделал правильный выбор."

    if pavel_history:
        "{i}(Он задерживает Аркадия за локоть — в первый раз в жизни.){/i}"
        voice "voice/pavel/ed6a628dd2762495.mp3"
        pavel "{i}(совсем другим тоном){/i} Ты знаешь про княгиню? От брата?.. Значит, ты всё-таки не чужой в этом доме. Я бы не хотел, чтобы он мне прочёл. Мне довольно того, что ты не прочёл."
        voice "voice/arcardy/34f33e7ffc9b5811.mp3"
        arcardy "Я и не прочитаю, дядюшка."
        voice "voice/pavel/935f3cded1b4ec6f.mp3"
        pavel "{i}(кивает, откашливается, отпускает его локоть){/i} Вот и хорошо. Женись, устраивайся… и не поминайте меня в письмах, когда будете вспоминать."
    else:
        voice "voice/arcardy/c61b244474c1d236.mp3"
        arcardy "Дядюшка, вы останетесь в Марьине?"
        voice "voice/pavel/410b5d1fe4210c4d.mp3"
        pavel "{i}(ровно){/i} Нет. Мне здесь нечего делать с тех пор, как у меня в дому поселилась любовь. Уеду в Дрезден, смотреть картины и быть полезным издалека."

    hide paveldef
    hide arcardiydef

    menu:
        "Остаться в Марьине: хозяйство, трое детей, тихая жизнь":
            $ kinship += 2
            $ play_narrator("36e81eba15ae1e31")
            "Аркадий остаётся. В пшенице он разбирается быстрее, чем в философии, и оказывается, что нигилиста в нём не было — был помещик с хорошим сердцем."
            "{i}(На его столе лежит портрет Базарова, и никто из гостей не знает, кто этот человек с резким лицом.){/i}"
        "Уехать с Катей в город: служить, печатать, быть нужным делу":
            $ nihil += 1
            $ kinship += 1
            $ play_narrator("fd959e3ee8457963")
            "Аркадий уезжает. Служба идёт скверно, потом отлично; печатать он так и не начинает, но заводит привычку читать про себя всё печатное и находить в нём смысл."
            "{i}(Катя говорит, что он стал добрее; он говорит, что стал полезнее; и оба остаются при своём мнении.){/i}"
        "Ничего не сказать Кате в саду — и уехать в Марьино":
            $ katya_branch = True
            jump scene_7_katya

    label story_after_wedding:

    # возврат из новой ветки: та же церковь в Марьине
    scene church_wedding at bg_kb
    with dissolve

    "{i}(Вскоре Павел Петрович уезжает за границу — совсем. Николай Петрович и Фенечка венчались тихо, без шума, как и хотели.){/i}"

    stop music fadeout 2.5

    jump scene_8


# ============================================================
# СЦЕНА 8. Эпилог — могила и развязка
# ============================================================
label scene_8:

    call chapter_card("ЭПИЛОГ · 2", "Могила") from _card8

    scene cemetery at bg_kb
    with fade

    play bgs "music/light-breeze.ogg" volume 0.25
    play music "music/waiting_theme.ogg" fadein 3.0 volume 0.3
    play sound "sounds/the-dry-cry-of-a-raven-and-incomprehensible-exclamations.ogg"

    $ play_narrator("2baf0a9386f6041c")
    "Сельское кладбище. Тихий летний вечер. На скромной могиле Базарова — свежие цветы."
    $ play_narrator("11f4ea04da0ad197")
    "Два старика — Василий Иванович и Арина Власьевна — стоят на коленях. Ветер шелестит листьями."

    show vasiliydef at left_char
    with dissolve
    show arinadef at right_char
    with dissolve

    voice "voice/vasiliy/1bfae786004386f6.mp3"
    vasiliy "{i}(у могилы, стоя на коленях){/i} Вот и всё… Евгений… Мой сын… Какой умный был… какой сильный…"

    voice "voice/arina/50adf0a217fde236.mp3"
    arina "{i}(плача тихо){/i} Он был такой добрый… такой талантливый… Почему Бог забрал его так рано…"

    voice "voice/vasiliy/2e3ad12ab474b22b.mp3"
    vasiliy "{i}(гладя могилу){/i} Мы будем приходить каждый день… Цветы сажать…"

    "{i}(Они не слышат шагов за спиной. Но на тропинке, у двух елей, стоит кто-то третий — и от того, чем кончится этот роман, не зависит уже ничего; зависит только то, как его прочтут.){/i}"

    stop music fadeout 2.0
    stop bgs fadeout 2.0

    # новые ветки: развязка своя, если игрок выбрал новую опцию в новой сцене
    if speta_branch:
        $ ending = "спета"
        jump ending_speta
    if hay_branch:
        $ ending = "ломоть"
        jump ending_loмоть
    if katya_branch:
        $ ending = "молчанье"
        jump ending_molchanie

    if anna_open >= 4:
        $ ending = "одна"
        jump ending_odtsova
    elif kinship >= nihil and kinship >= 3:
        $ ending = "дом"
        jump ending_life
    else:
        $ ending = "один"
        jump ending_alone


# ============================================================
# РАЗВЯЗКА 1. Живая жизнь
# ============================================================
label ending_life:

    scene cemetery at bg_kb_slow
    with fade

    play music "music/light-breeze.ogg" fadein 2.0 volume 0.5

    show arcardiydef at side_char
    with dissolve

    voice "voice/arcardy/d2aa234302c12ca3.mp3"
    arcardy "{i}(подходит, снимает шляпу; он не был здесь с похорон){/i} Василий Иванович… Арина Власьевна… Я тоже приехал."

    voice "voice/vasiliy/d48dc32473122296.mp3"
    vasiliy "{i}(встаёт с трудом){/i} Приехал! Вот и хорошо. Садись. Он тебя любил, а я тебя любил за то, что он тебя любил."

    voice "voice/arina/87f15d7ecc53fd48.mp3"
    arina "{i}(гладит его по руке){/i} Ты к нам приезжай, Аркадий Николаич. Мы тут, знаешь, о нём говорим. А тебе-то слушать приятнее, чем нам."

    "{i}(Аркадий остаётся на коленях дольше, чем собирался. Он не молится — он делает вид, что молится, и ему не стыдно.){/i}"

    hide arcardiydef
    hide vasiliydef
    hide arinadef
    with dissolve

    $ play_narrator("80017ead0da3f7b6")
    "Прошло ещё несколько лет."

    $ play_narrator("be2baf11508d30ea")
    "Аркадий и Катя живут в Марьине; у них трое детей, и Катя не изменилась ни на слово — она помнит и то, другим."
    $ play_narrator("10c1386f11ae3b50")
    "Николай Петрович кончает хозяйствовать и начинает переводить; Фенечка держит весь дом и смеётся громче всех."

    if saw_last_hours:
        $ play_narrator("5f2718b22d9b6775")
        "Аркадий до конца своих дней не может слышать слова «скорбный тиф» — и всегда приезжал в Васильевку, когда его звали, и ни разу не опоздал."
    else:
        $ play_narrator("05f34d5de0e692ea")
        "Аркадий до конца дней жалеет об одном: что не приехал в Васильевку раньше, чем его позвали, — и не приехал тогда, когда не позвали."

    if duel_warned:
        $ play_narrator("0a26136e8ed50743")
        "У Николая Петровича в ящике лежит письмо, которое он так и не показал Базарову. Он часто берёт его в руки и не открывает."

    if pavel_history:
        $ play_narrator("eefadda1ba05c5ef")
        "Павел Петрович живёт в Дрездене. Он всё-таки раз в год перечитывает своё прежнее письмо и пишет брату — коротко, о картинах, но пишет."
    else:
        $ play_narrator("8596b3303efa757d")
        "Павел Петрович живёт в Дрездене и пишет родным раз в год, коротко, о картинах."

    $ play_narrator("a351f1cf2cf347db")
    "А на могиле Базарова… только цветы и два старика, которые приходят каждый день."
    $ play_narrator("409083735850ddfc")
    "Не то, что он любил, осталось после него; осталось то, чего он не захотел: живая жизнь, которая сама разбирается со всем — без него и против него, и всё-таки по его дороге."

    $ play_narrator("19ac983aa551f9ad")
    "И жизнь продолжается."

    jump finale_card


# ============================================================
# РАЗВЯЗКА 2. Невозвратное (Одинцова)
# ============================================================
label ending_odtsova:

    scene nikolskoe at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 2.5 volume 0.4

    show annadef at center_char
    with dissolve

    $ play_narrator("ee7175e1aa5be43d")
    "Никольское. Поздний вечер. Анна Сергеевна одна в той же гостиной, где он сидел напротив, подвинув стул ближе, чем надо."

    voice "voice/anna/c21781528aa89fd6.mp3"
    anna "{i}(вслух, не поднимая глаз от неотправленного письма){/i} Я вышла замуж. Не за того, кого могла бы, а за того, кто был спокоен: человек хороший, законопослушный, с состоянием. Я берегла спокойствие — я его дождалась."

    "{i}(Она складывает письмо и не запечатывает его.){/i}"
    voice "voice/anna/ba75d2e40ca05023.mp3"
    anna "Один раз — только один — я была близка к тому, чтобы всё бросить и поехать к вам. Я не поехала, и вы умерли, и на этом всё кончилось."

    hide annadef

    "{i}(Проходит год. Анна Сергеевна приезжает на кладбище одна, без слуг, и не говорит старикам, кто она.){/i}"

    show annadef at right_char
    with dissolve
    show arinadef at left_char
    with dissolve

    voice "voice/anna/0ce381869e1038ef.mp3"
    anna "{i}(у могилы, в сторону стариков){/i} Я не знала, что здесь так тихо. Мне показалось бы это скукой, а теперь… нет."

    voice "voice/arina/9115ce386c8a28dd.mp3"
    arina "{i}(встаёт, крестится на неё, не зная кто){/i} Вы к кому, матушка?"

    voice "voice/anna/1bb24f166727821d.mp3"
    anna "{i}(долгая пауза){/i} К вашему сыну. Он меня не ждал. Я и сама не ждала, что приеду."

    if bazarov_spoke_all:
        voice "voice/vasiliy/8f845916d9d3937b.mp3"
        vasiliy "{i}(тихо, всё поняв по одному слову){/i} Он говорил про вас… в бреду… один раз. Он не назвал больше ни одного имени."
    else:
        voice "voice/vasiliy/ffd030c4d6e628fe.mp3"
        vasiliy "{i}(с достоинством){/i} Он о женщинах не говорил. Но он, знать, кого-то любил: в последние дни он просил не звать попов, а открыть окно. Он боялся, что не успеет посмотреть."

    hide annadef
    hide arinadef
    with dissolve

    $ play_narrator("4422b7229a505638")
    "Анна Сергеевна живёт с мужем статским советником, человеком добрым и рассудительным, и всю жизнь хранит в столе его записку в одну строку: «приезжайте; я жду, и мне скучно без вас»."
    $ play_narrator("97cf566215f279f1")
    "Она приезжает к этой могиле раз в несколько лет и всегда одна; молиться она не умеет, но стоит долго."

    if mercy >= 4:
        $ play_narrator("ccbe7d7fc5816199")
        "А старикам она каждый раз оставляет деньги на цветы и ни разу не называет своего имени — и они оба, не зная её, привыкают к этой даме в тёмной шляпе и ставят для неё стул у колодца."

    jump finale_card


# ============================================================
# РАЗВЯЗКА 3. Один в поле
# ============================================================
label ending_alone:

    scene theInn at bg_kb_slow
    with fade

    play music "music/waiting_theme.ogg" fadein 1.0 volume 0.5
    play bgs "music/light-breeze.ogg" volume 0.25

    $ play_narrator("1caa1575eb8b5842")
    "Тот же постоялый двор, десятью годами позже. Тот же запах ржаного хлеба из сеней — только дорога стала новее."

    show arcardiydef at center_char
    with dissolve

    voice "voice/arcardy/354fd981cf710c91.mp3"
    arcardy "{i}(входит в пальто, которое не его; смотрит, садится){/i} Я проезжал это место три раза и всякий раз ехал дальше. А теперь — сел."

    hide arcardiydef
    show bazarovdef at left_ghost
    with dissolve

    "{i}(Он видит перед собой не привидение, а привычку говорить вслух с тем, кого больше нет.){/i}"

    voice "voice/arcardy/ba29c133baad8edd.mp3"
    arcardy "Я не поехал к тебе тогда, Евгений. Я выбрал, что не надо путаться, и ты умер один, и я в этом не виноват, и виноват."

    voice "voice/bazarov/fc6649e76cc4fc19.mp3"
    bazarov "{i}(тихо, так, как он отвечал бы){/i} Не путай. Никто ни в чём не виноват. Ты был теплее меня — и прогадал на этом, или выиграл. Я не знаю. Я не дожил до ответа, а ты дожил и не нашёл."

    hide bazarovdef

    show arcardiydef at right_char
    with dissolve

    voice "voice/arcardy/216f932fa2da49ac.mp3"
    arcardy "Катя уехала к сестре. Папаша умер в прошлом году — тихо, как жил. Дядя пишет из Дрездена и не ждёт ответа. Я остался один в доме, который был полон."

    "{i}(Он достаёт из кармана засаленную книжку — ту самую, которую взял в Васильевке и не вернул.){/i}"

    voice "voice/arcardy/58434850cb3f79b5.mp3"
    arcardy "И всё-таки я не жалею, что смеялся над Козьным, и не жалею, что не смеялся. Я жалею, что не умел говорить вовремя ни там, ни здесь."

    menu:
        "Пойти на кладбище — и сказать вслух то, что не сказал":
            $ mercy += 1
            $ play_narrator("a2ace9cfb32f62b4")
            "Аркадий нанимает подводу и едет в Васильевку. На кладбище нет цветов; он рвёт их у забора и кладёт на плиту, сначала молча."
            voice "voice/arcardy/da71400bc689e2d5.mp3"
            arcardy "{i}(наконец){/i} Я пришёл. Не прощения просить — сказать, что ты был прав во всём, кроме одного: жизнь не пустая штука. Она пустая только для того, кто не остался."
            "{i}(Он приезжает в город и пишет письмо, которое отправляет, и получает ответ, который читает вслух.){/i}"
            $ play_narrator("879fe86f9fefc63f")
            "Это ещё не примирение, но уже не бегство."
        "Уехать, не сойдя с крыльца":
            $ nihil += 1
            "{i}(Аркадий платит хозяину, выходит на дорогу и идёт к станции, не оглядываясь.){/i}"
            $ play_narrator("247ea26bb59b1060")
            "Через неделю он в Петербурге; через год за границей; и всю жизнь едет быстрее, чем ездят из любопытства."
            $ play_narrator("91fff94b0c88e20f")
            "На его столе лежит та же книжка; он её не перечитывает, но и не выбрасывает — и в этом, а не в отъезде, и кончается его история."

    stop music fadeout 2.5
    stop bgs fadeout 2.5

    jump finale_card


# ============================================================
# ЗАКРЫВАЮЩИЙ КАДР
# ============================================================
label finale_card:

    scene black
    with fade

    play music "music/waiting_theme.ogg" fadein 2.0 volume 0.25

    "{i}(Последний голос принадлежит не им, а ему.){/i}"
    voice "voice/bazarov/bbcba9f1567d7eab.mp3"
    bazarov "{i}(в темноте, ровно, почти насмешливо){/i} Так вот как: разрушение — не дело. Дело — то, что вырастет на разрушенном. Мне не выросло. Вам — посмотрим."

    stop music fadeout 3.0

    scene black
    with fade

    if ending == "дом":
        centered "{size=64}{b}ЖИВАЯ ЖИЗНЬ{/b}{/size}\n\n{size=24}развязка 1 из 6 · по роману И. С. Тургенева «Отцы и дети»{/size}"
    elif ending == "одна":
        centered "{size=64}{b}НЕВОЗВРАТНОЕ{/b}{/size}\n\n{size=24}развязка 2 из 6 · по роману И. С. Тургенева «Отцы и дети»{/size}"
    elif ending == "спета":
        centered "{size=64}{b}ПЕСЕНКА СПЕТА{/b}{/size}\n\n{size=24}развязка 4 из 6 · по роману И. С. Тургенева «Отцы и дети»{/size}"
    elif ending == "ломоть":
        centered "{size=64}{b}ОТРЕЗАННЫЙ ЛОМОТЬ{/b}{/size}\n\n{size=24}развязка 5 из 6 · по роману И. С. Тургенева «Отцы и дети»{/size}"
    elif ending == "молчанье":
        centered "{size=64}{b}БЕЗЫМЯННОЕ ЧУВСТВО{/b}{/size}\n\n{size=24}развязка 6 из 6 · по роману И. С. Тургенева «Отцы и дети»{/size}"
    else:
        centered "{size=64}{b}ОДИН В ПОЛЕ{/b}{/size}\n\n{size=24}развязка 3 из 6 · по роману И. С. Тургенева «Отцы и дети»{/size}"

    return

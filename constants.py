#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Содержит сообщения для взаимодействия с пользователем
"""

from json import dumps


CMD_START_MSG = "Вас приветствует экспертная система Datatron!"

TELEGRAM_START_MSG = '''Я – экспертная система Datatron!

Со мной вы сможете быстро получать открытые финансовые данные. Расходы, доходы, дефицит, долг - не вопрос. Все это я знаю, и у меня есть данные как по России в целом, так и для любого ее региона.

*Особенности взаимодействия*
Datatron предоставляет данные по запросу на естественном языке в формате текстового или голосового сообщения.

*Текстовый режим*
Просто напишите собщение с интересующим вас вопросом.

*Голосовой режим*
Вопрос можно задать голосом, используя встроенную в Telegram запись аудио.

Если вы не знаете, что спросить, вы можете воспользоваться командой /idea. Подробное описание функций доступно по команде /help.

_Datatron – ваш личный эксперт в мире открытых финансовых данных!_'''

ABOUT_MSG = '''*Описание*
Datatron - личный ассистент, предоставляющий доступ к открытым финансовым данным России и её субъектов по запросам на естественном языке.

*Разработчики*
Студенты ФБМ и ФКН ВШЭ, а также ВМК МГУ и Финансового Универа, которые стараются изменить мир к лучшему.

*Данные*
Используются базы данных Единого портала бюджетной системы Российской Федерации и базы знаний Министерства финансов."

*Обратная связь*
Для нас важно ваше мнение о работе Datatron. Вы можете оставить отзыв о боте, написав его через пробел после команды /fb, или нажав кнопку "Оценить".

*Дополнительно:*
Использует [Yandex SpeechKit Cloud](https://tech.yandex.ru/speechkit/cloud/).'''

ABOUT_KEYBOARD = dumps({
    'inline_keyboard': [
        [
            {'text': 'Оценить', 'url': 'https://telegram.me/storebot?start=datatron_bot'}
        ],
        [
            {'text': 'Ознакомительный ролик', 'callback_data': 'intro_video'}
        ]
    ]
})

HELP_MSG = '''*Список доступных команд*
/start - Начало работы
/help - Помощь
/idea - Вопросы, которые задавали другие пользователи
/fb - Оставить отзыв
/about - О проекте

*Начало работы с Datatron*
Для поиска финансовой информации достаточно просто сформулировать и отправить свой запрос, например:

```
Объем внешнего долга России в 2016 году
Доходы федерального бюджета в 17 году
Исполнение бюджета Москвы по налогу на прибыль```

Также Datatron понимает голосовые запросы – просто отправьте ему голосовое сообщение. Всё устроено точно так же, как и текстовое общение.
'''

RESPONSE_QUALITY = dumps({
    'inline_keyboard': [
        [
            {'text': '👍', 'callback_data': 'correct_response'},
            {'text': '😒', 'callback_data': 'incorrect_response'}
        ],
    ]
})

ERROR_CANNOT_UNDERSTAND_VOICE = 'Не удалось распознать текст сообщения😥 Попробуйте еще раз!'
ERROR_NULL_DATA_FOR_SUCH_REQUEST = 'К сожалению, этих данных в системе нет🤕'
ERROR_SERVER_DOES_NOT_RESPONSE = 'К сожалению, сейчас сервис не доступен😩 Попробуйте снова чуть позже!'
ERROR_NO_DOCS_FOUND = 'Datatron не нашел ответ на ваш запрос :('

MSG_WE_WILL_FORM_DATA_AND_SEND_YOU = "Спасибо! Сейчас я сформирую ответ и отправлю его вам🙌"
MSG_NO_BUTTON_SUPPORT = 'Кнопочный режим более *не поддерживается*'
MSG_LEAVE_YOUR_FEEDBACK = 'Напишите после команды /fb ваш отзыв.\nНапример: `/fb Мне нравится, что...`'
MSG_WE_GOT_YOUR_FEEDBACK = 'Cпасибо! Ваш отзыв записан :)'
MSG_LOG_HISTORY_IS_EMPTY = 'Истории логов еще нет😔 Не растраивай Datatron, задай вопрос!'
MSG_USER_SAID_CORRECT_ANSWER = "Datatron приятно, что вы довольны ответом!"
MSG_USER_SAID_INCORRECT_ANSWER = 'Datatron извиняется и постарается стать лучше!'

# Constants for m2
ERROR_PARSING = 'Что-то пошло не так🙃 Проверьте ваш запрос на корректность'
ERROR_GENERAL = 'Что-то пошло не так🙃 Данные получить не удалось:('

HELLO = (
    'хай', 'привет', 'здравствуйте',
    'приветствую', 'прифки', 'дратути', 'hello'
)

HELLO_ANSWER = (
    'Привет!',
    'Здравствуйте! Самое время задать вопрос',
    'Приветствую!',
    'Привет-привет! Пришли за финансовыми данными? Задайте мне вопрос!',
    'Доброго времени суток! С вами Datatron😊'
)

HOW_ARE_YOU = (
    'как дела',
    'как поживаешь',
    'как жизнь',
    'как делишки',
    'как живешь'
)

HOW_ARE_YOU_ANSWER = (
    'У меня все отлично, спасибо',
    'Скучаю без твоих вопросов, спроси что-нибудь или нажми /idea',
    'Все хорошо! Дела идут в гору',
    'Замечательно!',
    '🔥',
    'Бывало и лучше! Без твоих запросов только и делаю, что прокрастинирую🙈',
    'Чудесно! Данные расходятся, как горячие пирожки!😄'
)

WHO_YOU_ARE = (
    'кто ты',
    'кто ты такой',
    'что ты',
    'что ты такое'
    'datatron',
    'дататрон'
    'расскажи про себя'
)

WHO_YOU_ARE_ANSWER = (
    ("Я – персональный помощник и экспертная система Datatron."
     "\n\nЯ работаю благодаря возможностям машинного обучения и могу ответить "
     "на тысячи вопросов о бюджете Российской Федерации и деятельности Минфина России."
     "\n\nА еще я скоро буду доступен как мобильное приложение"),
)

WHAT_CAN_YOU_DO = (
    'что ты знаешь',
    'что ты умеешь',
    'что ты можешь',
    'на что ты можешь ответить',
    'что знаешь',
    'что умеешь',
    'что можешь',
    'зачем ты'
)

WHAT_CAN_YOU_DO_ANSWER = (
    ("Я знаю очень много о *бюджете Российской Федерации*. Например, я могу ответить про расходы на высшее "
     "образование или культуру как в каждом субъекте Российской Федерации, так и в целом "
     "по федеральному бюджету. А также рассказать о доходах, внешнем и внутреннем долге."
     "\n\nЯ знаю о текущей *деятельности Министерства финансов* и его истории. Вы можете спросить "
     "меня об первом экономисте, годе основание Минфина России, самом молодом Министре, разработке "
     "бюджетного прогноза и еще сотни других вопросов!"
     "\n\nА еще я с легкостью дам *определения экономических терминов:* авизо, оферент, дебет, гистерезис и "
     "многих других."),
)

WHO_IS_YOUR_CREATOR = ('кто твой создатель', 'кто тебя создал')
WHO_IS_YOUR_CREATOR_ANSWER = (
    ("Меня создали студенты Высшей школы экономики, "
     "Московского Государственного Университета и Финансового Университета"),
)

EASTER_EGGS = {
    "давай встречаться": ("Это очень мило, но прости, на ближайшие несколько лет у меня другие планы",),
    "ты умный": ("Подлиза!", "Да, я не только симпатичная оболочка", "☺"),
    "в чем смысл жизни": ("Смысл жизни в том, чтобы размышлять над подобными вопросами",),
    "я тебя люблю": ("Я знаю.",),
    "ты веришь в бога": ("Простите, я не могу вести теологические дискуссии.",),
    "ты выйдешь за меня замуж?": ("Заманчивое предложение, но мне нужно его хорошенько обдумать.",),
    "ты глупая": ("Я становлюсь способнее с каждым днем",),
    "как ты выглядишь": ("Блестяще!",),
    "окей google": ("Эмм... мне кажется, вы ошиблись приложением",),
    "расскажи сказку": ("Что? Опять?",)
}

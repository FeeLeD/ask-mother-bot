import telebot
import chat
from typing import Optional, Dict

bot = telebot.TeleBot('5658408141:AAFQ414_EqGwnjj7wXH7ogXl30OmwyY266I')
data: Dict[str, int] = {}


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    data[username] = 0

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = telebot.types.KeyboardButton('Привет, Мам!')
    markup.add(start_button)
    bot.send_message(message.chat.id,
                     '<b>Привет!</b> 👋\n\nЭтот бот поможет вам научиться проводить интервью с потенциальными '
                     'клиентами и понять, какие вопросы нужно задавать, чтобы извлечь из них выгоду.\n\nДавайте '
                     'представим, что вы ведете разговор с мамой, чтобы понять, что можно узнать о вашей бизнес-идее '
                     '— <i>цифровой кулинарной книге для iPad</i> 🍭\n\nВам будут предложены варианты вопросов, '
                     'которые вы могли бы задать своей маме, чтобы сделать выводы о востребованности вашей '
                     'бизнес-идеи.\n\nСимулятор будет вам отвечать, а также давать комментарии к вашему вопросу.',
                     parse_mode='HTML',
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    username = message.from_user.username
    response = chat.get_response_from(message)

    if response is None:
        bot.send_message(message.chat.id, 'Что-то пошло не так...')
        return None

    if response.is_bad_input:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите вопрос из предложенных вариантов 👀')
        return None

    if response.current_question is not None and response.current_question.is_good_question:
        if username in data:
            data[username] += 1

    markup: Optional[telebot.types.ReplyKeyboardMarkup] = None
    if response.question1 is not None and response.question2 is not None:
        markup = telebot.types.ReplyKeyboardMarkup()
        first_button = telebot.types.KeyboardButton(response.question1.text)
        second_button = telebot.types.KeyboardButton(response.question2.text)
        markup.add(first_button)
        markup.add(second_button)

    answer = response.answer.text
    if response.answer.key == 1:
        answer = 'Привет, {}!'.format(message.from_user.first_name)

    bot.send_message(message.chat.id, answer, reply_markup=markup)
    if hasattr(response.answer, 'comment'):
        if response.current_question.is_good_question:
            question_estimation = '<i>Хороший вопрос!</i> 🚀\n'
        else:
            question_estimation = '<i>Плохой вопрос...</i> 🙃\n'

        bot.send_message(message.chat.id,
                         '<b>Комментарий</b>\n{}{}'.format(question_estimation, response.answer.comment),
                         parse_mode='html')

    if hasattr(response.answer, 'is_final_answer') and response.answer.is_final_answer:
        if username not in data:
            return None

        if data[username] > 2:
            final_results = 'Отличная работа! 🎉\n\nВы получили хорошее представление о вашем клиентском сегменте и ' \
                            'ряд ценных идей для дальнейшего анализа. Это был полезный разговор!'
        else:
            final_results = 'Кажется, вы задали слишком много неудачных вопросов... 😔\n\nЕсли вы проведете еще ' \
                            'несколько ' \
                            'бесед в подобном духе, всё более убеждаясь в своей правоте, то будете долго удивляться, ' \
                            'почему никто (включая вашу маму) не покупает это приложение, особенно принимая во ' \
                            'внимание то, как тщательно вы всё продумали.\n\nДелать не правильно в данном случае ' \
                            'хуже, чем не делать ничего вообще. Осознав, что вам мало что понятно, вы будете вести ' \
                            'себя более осмотрительно. Нет смысла получать ложные подтверждения своей правоты. С ' \
                            'таким же успехом можно убеждать пьяного, что он трезв — это ничем не улучшит ' \
                            'ситуацию.\n\nБеседу с потенциальным клиентом можно построить более правильно, даже мама ' \
                            'может помочь нам понять, насколько хороша наша бизнес-идея. '

        markup = telebot.types.ReplyKeyboardMarkup()
        button = telebot.types.KeyboardButton('/start')
        markup.add(button)

        bot.send_message(message.chat.id,
                         '<b>Результат</b>\n<i>Задано хороших вопросов:</i> {}\n{}'.format(data[username],
                                                                                           final_results),
                         parse_mode='html',
                         reply_markup=markup)


bot.polling(none_stop=True, interval=0)

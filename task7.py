import os

from dotenv import load_dotenv
from pytimeparse import parse

import ptbot


def timer(chat_id, message, bot):
    time = parse(message)
    message_id = bot.send_message(chat_id, 'Запускаю таймер')
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        time=time,
        bot=bot,
    )
    bot.create_timer(
        time,
        timeout,
        chat_id=chat_id,
        message=message,
        bot=bot,
    )


def notify_progress(secs_left, chat_id, message_id, time, bot):
    bot.update_message(
        chat_id,
        message_id,
        'Осталось {0} секунд\n{1}'.format(secs_left,render_progressbar(time, time-secs_left))
    )


def timeout(chat_id, message, bot):
    bot.send_message(chat_id, 'Время вышло!')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(timer, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
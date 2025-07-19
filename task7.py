import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse
from decouple import config


load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
bot = ptbot.Bot(TG_TOKEN)


def timer(chat_id, message):
    time = parse(message)
    message_id = bot.send_message(chat_id, 'Запускаю таймер')
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        time=time,
    )
    bot.create_timer(
        time,
        timeout,
        chat_id=chat_id,
        message=message,
    )


def notify_progress(secs_left, chat_id, message_id, time):
    bot.update_message(
        chat_id,
        message_id,
        'Осталось {0} секунд\n{1}'.format(secs_left,render_progressbar(time, time-secs_left))
    )


def timeout(chat_id, message):
    bot.send_message(chat_id, 'Время вышло!')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot.reply_on_message(timer)
    bot.run_bot()


if __name__ == '__main__':
    main()

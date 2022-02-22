from telegram.ext import Updater, CommandHandler
import config as cg
import logging
import clanbattle

root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# @run_async
# def send_async(context, *args, **kwargs):
#     context.bot.send_message(*args, **kwargs)


def main():
    bot = Updater(token=cg.TOKEN, request_kwargs={'proxy_url': cg.proxy_url}, use_context=True)
    bot.job_queue.run_repeating(clanbattle.stage_data, 1800, first="2022-01-21 8:01:00", last="2022-02-27 23:51:00")
    bot.start_polling()


if __name__ == '__main__':
    main()

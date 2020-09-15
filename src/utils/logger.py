import logging

bot_logger = logging.getLogger('bot')
bot_logger.setLevel(logging.INFO)
bot_logger_handler = logging.StreamHandler()
bot_logger_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
bot_logger.addHandler(bot_logger_handler)

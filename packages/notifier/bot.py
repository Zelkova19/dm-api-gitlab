import os
from pathlib import Path
from telebot import TeleBot
from vyper import v

config = Path(__file__).parent.joinpath("../../").joinpath("config")
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()


# def send_file() -> None:
#     telegram_bot = TeleBot(v.get("telegram.token"))
#     file_path = Path(__file__).parent.joinpath("../..").joinpath("swagger-coverage-report.html")
#     with open(file_path, "rb") as document:
#         telegram_bot.send_document(v.get("telegram.chat_id"), document=document, caption="coverage")

def send_file():
    telegram_bot = TeleBot(v.get("telegram.token"))
    print("Current working directory:", os.getcwd())
    file_path = "../../swagger-coverage-report.html"
    absolute_path = os.path.abspath(file_path)
    print(f"Attempting to open file at: {absolute_path}")
    try:
        with open(absolute_path, "rb") as document:
            telegram_bot.send_document(v.get("telegram.chat_id"), document=document, caption="coverage")
    except Exception as e:
        print(f"An error occurred while sending the file: {e}")


if __name__ == "__main__":
    send_file()

import json

import telebot
from pyexpat.errors import messages
from telebot import types
from messages import *
from markups import start_markup, question_markup
from commands import *
import json


TOKEN = "7916982387:AAGCKNHYXEvNcXrD-ux_xFdVHpzHrWJzkao"

bot = telebot.TeleBot(TOKEN)
def send_question(message, question_id):
    question = list(questions[question_id].keys())[0]
    answers = questions[question_id][question].get("answers")
    image = f"media/{question[question_id][question].get('image')}"
    with open(image, "rb") as photo:
        bot.send_photo(message.chat.id, caption=question, photo=photo, reply_markup=question_markup(question_id, answers))
    description = questions[question_id][question].get("description")
def get_questions():
    with open("questions.json", encoding="UTF-8") as file:
        return json.load(file)
questions = get_questions()
@bot.message_handler(commands=["start"])
def start(message: types.Message):
    bot.send_message(message.chat.id,START_MESSAGE, reply_markup=start_markup())
@bot.message_handler(content_types=["text"])
def handler(message: types.Message):
    if message.text == START_QUIZ:
        send_question(message, question_id=0)

@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call:types.CallbackQuery):
    data = json.loads(call.data)
    question_id = data.get("question_id")
    answer_id = data.get("answer_id")
    description = questions[question_id][call.message.text].get("description")
    if answer_id == 0:
        bot.send_message(call.message.chat.id, TRUE_ANSWER)
    else:
        text = f"{FALSE_ANSWER}\n{description}"
        bot.send_message(call.message.chat.id, text)
    if len(questions)-1 == question_id:
        bot.send_message(call.message.chat.id, END_QUIZ)
    else:
        send_question(call.message, question_id+1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
if __name__ == "__main__":
    bot.infinity_polling()








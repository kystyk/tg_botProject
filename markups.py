from telebot import types
from commands import *
import json
import random

def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    quiz_button = types.KeyboardButton(START_QUIZ)
    markup.add(quiz_button)
    return markup

def question_markup(question_id ,answers: list):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for i, answer in enumerate(answers):
        buttons.append(types.InlineKeyboardButton(answer, callback_data=json.dumps({
            "question_id": question_id,
            "answer_id": i
        })))
    random.shuffle(buttons)
    markup.add(*buttons)
    return markup
import json
import os
DICT_DATA = 'data/quiz_data.json'
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    # 2 вопрос
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    # 3 вопрос
    {
        "question": "Как правильно объявить комментарий в Python?",
        "options": ["// comment", "# comment", "<!-- comment -->", "; comment"],
        "correct_option": 1
    },
    # 4 вопрос
    {
        "question": "Что такое переменная в Python?",
        "options": ["Место для хранения данных", "Имя программы", "Вид экрана", "Параметр компилятора"],
        "correct_option": 0
    },
    # 5 вопрос
    {
        "question": "Что выводит оператор print() в Python?",
        "options": ["Только текст", "Любые типы данных", "Исключительно числа", "Только списки"],
        "correct_option": 1
    },
    # 6 вопрос
    {
        "question": "Какой тип данных предназначен для хранения вещественных чисел в Python?",
        "options": ["float", "double", "real", "decimal"],
        "correct_option": 0
    },
    # 7 вопрос
    {
        "question": "Как называется цикл, позволяющий повторять инструкцию определенное количество раз?",
        "options": ["for", "while", "do while", "repeat until"],
        "correct_option": 0
    },
    # 8 вопрос
    {
        "question": "Какая функция возвращает длину последовательности?",
        "options": ["length()", "size()", "len()", "count()"],
        "correct_option": 2
    },
    # 9 вопрос
    {
        "question": "Какой секретный режим есть в интерпретаторе Python?",
        "options": ["Режим спящего дракона", "Игровой режим", "Тайный режим шутера", "Режим паскаля"],
        "correct_option": 0
    },
    # 10 вопрос
    {
        "question": "Почему программа на Python иногда сравнивается с поэзией?",
        "options": ["Код легко читается и воспринимается людьми", "Python создаёт красивые узоры", "Программы работают быстрее остальных", "Нет правильного ответа"],
        "correct_option": 0
    }
]

# Создаем каталог data, если он не существует
os.makedirs(os.path.dirname(DICT_DATA), exist_ok=True)

with open(DICT_DATA, 'w') as file:
     json.dump(quiz_data, file)
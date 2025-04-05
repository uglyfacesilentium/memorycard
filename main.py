#создай приложение для запоминания информации
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QButtonGroup)
from random import randint, shuffle

class Question:
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        #все объекты надо задать при создании объекта, они запоминаются в свойства
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

questions_list = []
questions_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский'))
questions_list.append(Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий'))
questions_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))

app = QApplication([])

btn = QPushButton('Ответить') #кнопка ответа
lb_Question = QLabel('Самый сложный вопрос в мире!') #текст вопроса

RadioGroupBox = QGroupBox('Варианты ответов') #группа на экране для переключателей с ответами
afa1 = QRadioButton('Вариант 1')
afa2 = QRadioButton('Вариант 2')
afa3 = QRadioButton('Вариант 3')
afa4 = QRadioButton('Вариант 4')

RadioGroup = QButtonGroup() #это для группировки переключателей, чтобы управлять их поведением
RadioGroup.addButton(afa1)
RadioGroup.addButton(afa2)
RadioGroup.addButton(afa3)
RadioGroup.addButton(afa4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout() #все вертикальные будут внутри горизонтального
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(afa1)#два ответа в первый столбец
layout_ans2.addWidget(afa2)
layout_ans3.addWidget(afa3)#два ответа во второй столбец
layout_ans3.addWidget(afa4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) #разместили столбцы в одной строке

RadioGroupBox.setLayout(layout_ans1) #готова "панель" с вариантами ответов

AnsGroupBox = QGroupBox('Результат теста')
rez = QLabel('Правильно/Неправильно') #здесь размещается надпись правильно или неправильно
corr = QLabel('Правильный ответ')

layout_res = QVBoxLayout()
layout_res.addWidget(rez, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(corr, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)

layout_line1 = QHBoxLayout() #вопрос 
layout_line2 = QHBoxLayout() #варианты ответов или результат теста
layout_line3 = QHBoxLayout() # кнопка ответить

layout_line1.addWidget(lb_Question, alignment = (Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide() #скроем панель с ответом, сначал должна быть видна панель вопросов

layout_line3.addStretch(1)
layout_line3.addWidget(btn, stretch=2) #кнопка должна быть большой
layout_line3.addStretch(1)

layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) #пробелы между содержимым

def show_result(): #показать панель ответов
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn.setText('Следующий вопрос')

def show_question(): #показать панель вопросов
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn.setText('Ответить')
    RadioGroup.setExclusive(False) #сняли ограничение чтобы можно было сбросить выбор радиокнопки радиобаттон
    afa1.setChecked(False)
    afa2.setChecked(False)
    afa3.setChecked(False)
    afa4.setChecked(False)
    RadioGroup.setExclusive(True) #вернули ограничения теперь только одна радиокнопка может быть выбрана

answers = [afa1, afa2, afa3, afa4]

def ask(q: Question):
    #функция записывает значения вопроса и ответов в соответствующие виджеты, при этом варианты ответов располагаются случайным образом
    shuffle(answers) #перемешали список из кнопок, теперь на первом месте списка какая то непредсказуемая кнопка
    answers[0].setText(q.right_answer) #первый элемент из списка заполним правильным ответом, остальные заполняем неверными вариантами ответов
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question) #вопрос
    corr.setText(q.right_answer)#ответ
    show_question()#показываем панель вопросов

def show_correct(res):
    #показать результат - установим переданный текст в надпись результат и покажем нужную панель
    rez.setText(res)
    show_result()

def check_answer():
    #если выбран какой то вариант ответа, то его надо проверить и показать панель ответов
    if answers[0].isChecked():
        show_correct('Правильно!')
        window.score += 1
        print('Статистика\n-Всего вопросов:', window.total, '/n-Правильных ответов:', window.score)
        print('Рейтинг: ', (window.score/window.total*100), '%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Неверно!')

def next_question():
    #задаёт вопрос из списка
    window.total += 1
    print('Статистика\n-Всего вопросов:', window.total, '\n-Правильных ответов:', window.score)
    cur_question = randint(0, len(questions_list) - 1)
    q = questions_list[cur_question] #взяли вопрос
    ask(q)#спросили

def click_OK():
    #определяет надо ли показывать другой вопрос или проверить ответ на этот
    if btn.text() == 'Ответить':
        check_answer() #проверка ответа
    else:
        next_question()# следующий вопрос

window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memory Card')

btn.clicked.connect(click_OK) #по нажатии на кнопку выбираем, что конкретно происходит

#все настроено, осталось задать вопрос и показать окно:
window.score = 0
window.total = 0
next_question()
window.resize(400, 300)
window.show()
app.exec()
from design import *
from datetime import date, time



class CreationWindow(QtWidgets.QMainWindow): # второе окно для выбора параметров заметки
    def __init__(self, main_win, notes, scrollLayout):
        super().__init__()
        self.setWindowTitle('Creation')
        self.setFixedSize(500, 600)
        self.setStyleSheet('background-color:rgb(40, 40, 40)')

        self.notes = notes
        self.scrollLayout = scrollLayout
        self.main_win = main_win

        layout = QtWidgets.QVBoxLayout()

        w = QtWidgets.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        self.note_type_tip = QtWidgets.QLabel('Тип заметки:')
        self.note_type_tip.setFixedSize(150, 20)
        self.note_type_tip.setStyleSheet('color:rgb(215, 215, 215)')

        layout.addWidget(self.note_type_tip)

        self.note_type = QtWidgets.QComboBox()
        self.note_type.setFixedSize(175, 20)
        self.note_type.addItems(['Simple note', 'Note with progress bar', 'Task', 'Reminder'])
        self.note_type.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(215, 215, 215);border-radius:3px')
        self.note_type.currentIndexChanged.connect(self.type_changed)

        layout.addWidget(self.note_type)

        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText('Название')
        self.name.setFixedSize(175, 20)
        self.name.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(215, 215, 215);border-radius:3px')

        layout.addWidget(self.name)


        self.note_mes = QtWidgets.QTextEdit()
        self.note_mes.setPlaceholderText('Введите текст...')
        self.note_mes.setFixedSize(300, 200)
        self.note_mes.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(215, 215, 215);border-radius:5px')

        layout.addWidget(self.note_mes)

        self.reminder_date_tip = QtWidgets.QLabel('Дата:')
        self.reminder_date_tip.setFixedSize(120, 20)
        self.reminder_date_tip.setStyleSheet('color:rgb(215, 215, 215)')

        layout.addWidget(self.reminder_date_tip)

        self.reminder_date = QtWidgets.QDateEdit()
        self.reminder_date.setFixedSize(175, 20)
        self.reminder_date.setDate(date.today())
        self.enabled(self.reminder_date, False)
        self.reminder_date.setEnabled(False)

        layout.addWidget(self.reminder_date)

        self.count_tip = QtWidgets.QLabel('Количество:')
        self.count_tip.setFixedSize(120, 20)
        self.count_tip.setStyleSheet('color:rgb(215, 215, 215)')

        layout.addWidget(self.count_tip)

        self.count = QtWidgets.QSpinBox()
        self.count.setFixedSize(175, 20)
        self.count.setRange(1, 1000)
        self.enabled(self.count, False)
        self.count.setEnabled(False)

        layout.addWidget(self.count)


        self.conf_but = QtWidgets.QPushButton()
        self.conf_but.setText('OK')
        self.conf_but.setFixedSize(483, 40)
        self.conf_but.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(215, 215, 215);border-radius:5px')
        self.conf_but.setCheckable(True)
        self.conf_but.clicked.connect(self.creation)

        layout.addWidget(self.conf_but)

        # 247, 69, 81



    def setValue(self, value, maximum):
        self.progress_bar.setValue(value)
        self.progress_bar.setMaximum(maximum)
        self.label.setText(f"{value}/{maximum}")

    def type_changed(self):
        match self.note_type.currentText():
            case 'Reminder':
                self.enabled(self.reminder_date, True)
                self.reminder_date.setEnabled(True)
                self.count.clear()
                self.enabled(self.count, False)
                self.count.setEnabled(False)

            case 'Note with progress bar':
                self.enabled(self.count, True)
                self.count.setEnabled(True)
                self.reminder_date.setDate(date.today())
                self.enabled(self.reminder_date, False)
                self.reminder_date.setEnabled(False)
            case _:
                self.reminder_date.setDate(date.today())
                self.enabled(self.reminder_date, False)
                self.reminder_date.setEnabled(False)
                self.count.clear()
                self.enabled(self.count, False)
                self.count.setEnabled(False)

    def enabled(self, object, flag): # "анимация" включен виджет или нет
        if flag:
            object.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(215, 215, 215);border-raduis:3px')
        else:
            object.setStyleSheet('background-color:rgb(200, 200, 200);border-radius:3px')


    def creation(self):   # создание нового словаря в json-файле
        if self.note_mes.toPlainText() != '':
            self.name.setText(self.name.text().strip())
            if self.name.text() == '':
                self.name.setText(self.note_mes.toPlainText().split('\n')[0][:25])

            with open('info.json', encoding='UTF-8') as file:
                temp = json.load(file)

            par_3 = None
            match self.note_type.currentText():
                case 'Simple note':
                    par_3 = None
                case 'Note with progress bar':
                    par_3 = int(self.count.text())
                case 'Task':
                    par_3 = True
                case 'Reminder':
                    par_3 = f"{self.reminder_date.date().toString('dd-MM-yyyy')}"



            temp.append({'name': self.name.text(), 'mes': self.note_mes.toPlainText(), 'par_3': par_3})

            with open('info.json', 'w', encoding='UTF-8') as file:
                json.dump(temp, file)
            print(temp[0]['name'])
            print(len(temp))
            add_note(self.name.text(), self.note_mes.toPlainText(), par_3, self.notes, self.scrollLayout)
            self.close()
           #self.main_win.refresh_window()



def add_note(name, mes, par_3, list, lay):
    temp = QtWidgets.QWidget()
    temp.setStyleSheet('background-color:rgb(0, 0, 0);border-radius:10px')
    temp.setFixedSize(400, 450)
    font = QtGui.QFont()
    font.setPointSize(18)

    layout = QtWidgets.QVBoxLayout()

    title = QtWidgets.QLabel(temp)
    title.setText(name + '\n')
    title.setStyleSheet('color:rgb(255, 255, 255)')
    title.setFont(font)
    layout.addWidget(title)

    if type(par_3) == type('s'):
        date_label = QtWidgets.QLabel(temp)
        date_label.setText('Дата:'+par_3)
        date_label.setStyleSheet('color:rgb(255, 255, 255)')
        font.setPointSize(12)
        date_label.setFont(font)
        layout.addWidget(date_label)
        if date.today().strftime('%d-%m-%Y') == par_3:
            print('dadaadad')


    text = QtWidgets.QTextBrowser(temp)
    text.setPlainText(mes)
    text.setMinimumSize(200, 100)
    text.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(255, 255, 255)')
    text.setReadOnly(True)


    layout.addWidget(text)

    if type(par_3) == type(True):
        lcd_display = QtWidgets.QLCDNumber(temp)
        lcd_display.setDigitCount(8)  # 8 цифр: HH:MM:SS
        lcd_display.setFixedSize(140, 30)
        layout.addWidget(lcd_display)

        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: update_lcd(lcd_display))
        timer_value = QtCore.QTime(0, 0)  # Начальное значение таймера: 00:00:00
        timer_started = False

        def start_or_stop_timer():
            nonlocal timer_started
            if not timer_started:
                timer_started = True
                timer.start(1000)  # Запустите таймер с интервалом в 1 секунду
            else:
                timer.stop()
                timer_started = False

            if start_but.text() == 'Старт':
                start_but.setText('Стоп')
            else:
                start_but.setText('Старт')

        def update_lcd(display):
            nonlocal timer_value
            timer_value = timer_value.addSecs(1)
            display.display(timer_value.toString("hh:mm:ss"))

        start_but = QtWidgets.QPushButton('Старт', temp)
        start_but.setStyleSheet('background-color:rgb(40, 40, 40);color:rgb(255, 255, 255)')
        start_but.setFixedHeight(30)
        layout.addWidget(start_but)

        start_but.clicked.connect(start_or_stop_timer)

    if type(par_3) == type(1):
        pb_layout = QtWidgets.QHBoxLayout()
        but1 = QtWidgets.QPushButton('-', temp)
        but1.setFixedSize(50, 20)
        but1.setStyleSheet('background-color:rgb(40, 40, 40);color:rgb(255, 255, 255);border-radius:5px')
        pb_layout.addWidget(but1)

        prog_bar = QtWidgets.QProgressBar(temp)
        prog_bar.setStyleSheet('background-color:rgb(40, 40, 40);color:rgb(255, 255, 255)')
        prog_bar.setMaximum(par_3)
        prog_bar.setValue(0)
        pb_layout.addWidget(prog_bar)

        but2 = QtWidgets.QPushButton('+', temp)
        but2.setFixedSize(50, 20)
        but2.setStyleSheet('background-color:rgb(40, 40, 40);color:rgb(255, 255, 255);border-radius:5px')
        pb_layout.addWidget(but2)
        layout.addLayout(pb_layout)

        but1.clicked.connect(lambda: decrease_progress(prog_bar))
        but2.clicked.connect(lambda: increase_progress(prog_bar))


    # Создаем горизонтальный макет для кнопок
    button_layout = QtWidgets.QHBoxLayout()

    # Создаем и добавляем три кнопки в горизонтальный макет

    del_button = QtWidgets.QPushButton('Удалить', temp)
    del_button.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(255, 255, 255);border-radius:5px')
    button_layout.addWidget(del_button)

    pin_button = QtWidgets.QPushButton('Закрепить', temp)
    pin_button.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(255, 255, 255);border-radius:5px')
    button_layout.addWidget(pin_button)

    # Создаем вертикальный макет и добавляем элементы

    layout.addLayout(button_layout)  # Добавляем горизонтальный макет с кнопками

    temp.setLayout(layout)

    list.append(temp)
    list[-1].setObjectName('note' + str(len(list) - 1))

    # Добавляем виджет-контейнер в QGridLayout
    row = len(list) // 10
    col = len(list) % 10

    lay.addWidget(temp, row, col)








def decrease_progress(progress_bar):
    if progress_bar.value() > 0:
        progress_bar.setValue(progress_bar.value() - 1)

def increase_progress(progress_bar):
    if progress_bar.value() < progress_bar.maximum():
        progress_bar.setValue(progress_bar.value() + 1)







def test():
    print('rabotaee')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()

    ui = Ui_window()
    ui.setupUi(window)

    window.show()


    sys.exit(app.exec_())


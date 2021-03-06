import sys
import getpass
import sqlite3
import requests
from note import Note
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджета
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QDialog, QPlainTextEdit, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QBoxLayout, QDesktopWidget, QInputDialog, QLineEdit, QMessageBox, QAction, QTableWidget
from PyQt5.Qt import Qt, QFont
from PyQt5 import QtGui

SERVER_IP = "https://vk.com"
SERVER_PORT = "80"


# Функция для центрирования окна по экрану устройства
def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())


# Унаследуем наш класс от простейшего графического примитива QWidget
class SmartNotes(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 300)
        center(self)

        self.pixmap = QPixmap("a.png")
        self.image = QLabel(self)

        self.setStyleSheet("""
                QPushButton {
                        font: 75 10pt "Microsoft YaHei UI";
                        font-weight: bold;
                        color: rgb(255, 255, 255);
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                        y2:0, stop:0 rgb(255, 136, 0), stop:1 rgb(250, 200, 0));
                        border-style: solid;
                        border-radius:10px;
                }
                QPushButton:hover {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                            y2:0, stop:0 rgb(255, 170, 0), stop:1 rgb(250, 200, 0));
                        }
                        """)

        # Настройка окна
        self.setWindowTitle("SmartNotes")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(700, 300)
        # Создание объектов на экране
        self.btn_new = QPushButton("Новая заметка")
        self.btn_new.setMinimumSize(200, 35)

        self.btn_new.setFont(QFont("Arial", 15))
        self.btn_new.clicked.connect(self.new_note)
        self.btn_del = QPushButton("Изменить заметки")
        self.btn_del.setMinimumSize(200, 35)

        self.btn_del.setFont(QFont("Arial", 15))
        self.btn_del.clicked.connect(self.del_note)

        self.lable_main = QLabel("SmartNotes")
        self.lable_main.setFont(QFont("Arial", 60))

        # Создание сеток дабы центрировать объекты на экране
        self.box_btn = QBoxLayout(1)
        self.box_btn.addWidget(self.btn_del)
        self.box_btn.addWidget(self.btn_new)
        self.box_btn.setAlignment(Qt.AlignCenter)

        self.box_label = QBoxLayout(1)

        self.box_label.addWidget(self.lable_main)
        self.box_label.setAlignment(Qt.AlignCenter)

        self.box_box = QVBoxLayout()
        self.box_box.addLayout(self.box_label)
        self.box_box.addLayout(self.box_btn)
        self.box_label.addWidget(self.image)
        self.box_box.setAlignment(Qt.AlignCenter)

        self.setLayout(self.box_box)
        self.image.setPixmap(self.pixmap)

    def new_note(self):
            self.note = CreateNote()
            self.note.exec()

    def del_note(self):
        self.note = EditNote()
        self.note.exec()


class CreateNote(QDialog):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        self.path = ""
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 500, 300)
        center(self)

        # Настройка окна
        self.setWindowTitle("SmartNotes – Новая заметка")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(500, 300)

        # Создание интерфейсов
        self.title_lable = QLabel(self)
        self.title_lable.setText("Заголовок заметки:")

        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText("Не забыть!")

        self.text_lable = QLabel(self)
        self.text_lable.setText("Текст заметки:")

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setPlaceholderText("1) Покормить рыбок\n2) Сделать домашнее задание")

        self.pic_lable = QLabel(self)
        self.pic_lable.setText("Картинка в заметке:")

        self.pic_button = QPushButton(self)
        self.pic_button.setText("Выбрать картинку")
        self.pic_button.clicked.connect(self.picture)

        self.author_lable = QLabel(self)
        self.author_lable.setText("Автор заметки:")

        self.author_edit = QLineEdit(self)
        self.author_edit.setPlaceholderText(getpass.getuser())

        self.btn_ready = QPushButton(self)
        self.btn_ready.setText("Готово!")
        self.btn_ready.clicked.connect(self.ready)

        self.box = QVBoxLayout(self)
        self.box.addWidget(self.title_lable)
        self.box.addWidget(self.title_edit)
        self.box.addWidget(self.text_lable)
        self.box.addWidget(self.text_edit)
        self.box.addWidget(self.pic_lable)
        self.box.addWidget(self.pic_button)
        self.box.addWidget(self.author_lable)
        self.box.addWidget(self.author_edit)
        self.box.addWidget(self.btn_ready)
        self.setLayout(self.box)

    def picture(self):
        self.path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '',
                                                'Картинка (*.jpg);;Картинка (*.jpg);;Все файлы (*)')[0]

    def ready(self):
        if not self.text_edit.toPlainText() or not self.author_edit.text() or not self.author_edit.text():
            self.msg_box = QMessageBox(self)
            self.msg_box.setWindowTitle("Ошибка!")
            self.msg_box.setText("Заполните все поля!")
            self.msg_box.exec()
        else:
            res, okpressed = QInputDialog.getItem(self, "SmartNotes – Новая заметка",
                                                  "Выберете действие?", ["Предпросмотр", "Создать"], 0, False)
            if okpressed and res == "Предпросмотр":
                self.newnote = Note(self.title_edit.text(), self.author_edit.text(), self.text_edit.toPlainText(),
                                    self.path)
                self.newnote.exec()
            if okpressed and res == "Создать":
                con = sqlite3.connect("notes.db")
                # Создание курсора
                cur = con.cursor()
                # Выполнение запроса и получение всех результатов
                try:
                    cur.execute(f'INSERT INTO notes (noteTitle, noteAuthor) VALUES ("{self.title_edit.text()}", '
                                f'"{self.author_edit.text()}")')
                    con.commit()
                    cur.execute(f'INSERT INTO texts (noteId, noteText, notePic) VALUES ((SELECT last_insert_rowid()), '
                                f'"{self.text_edit.toPlainText()}", "{self.path}")')
                    con.commit()
                    cur.execute(f'INSERT INTO times (noteId, noteCreateTime, noteRemoveTime) '
                                f'VALUES ((SELECT last_insert_rowid()), NULL, NULL)')
                    con.commit()
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setWindowTitle("Успешно!")
                    self.msg_box.setText("Заметка создана!")
                    self.msg_box.exec()
                except Exception:
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setWindowTitle("Ошибка!")
                    self.msg_box.setText("Заметка не создана!")
                    self.msg_box.exec()
                # Закрытие подключения
                con.close()


class EditNote(QDialog):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 500, 300)
        center(self)

        # Настройка окна
        self.setWindowTitle("SmartNotes – Изменить заметки")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(500, 300)

        self.table = QTableWidget(self)

        self.box = QBoxLayout(0)
        self.setLayout(self.box)


class MainApp(QMainWindow):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 300)
        center(self)
        self.setWindowTitle("SmartNotes")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(700, 300)

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&Настройки')
        self.save = QAction("Оцените приложение", self)
        self.fileMenu.addAction(self.save)
        self.save.triggered.connect(self.rating)

    def rating(self):
        rate, ok = QInputDialog.getInt(self, 'Оцените SmartNotes', 'Введите оценку от 1 до 5', 0, 1, 5)
        if ok:
            req = requests.get(SERVER_IP+"/rateapp?rating=" + str(rate), SERVER_PORT)
            if req.status_code == 200:
                self.msg_box = QMessageBox(self)
                self.msg_box.setWindowTitle("Успешно!")
                self.msg_box.setText("Ваш отзыв был отправлен!")
                self.msg_box.exec()
            else:
                self.msg_box = QMessageBox(self)
                self.msg_box.setWindowTitle("Ошибка!")
                self.msg_box.setText("Отсутствует связь с сервером, попробоуйте позже.")
                self.msg_box.exec()



if __name__ == '__main__':
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # А теперь создадим и покажем пользователю экземпляр
    # нашего виджета класса Example
    ex = MainApp()
    notess = SmartNotes()
    ex.setCentralWidget(notess)
    ex.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())

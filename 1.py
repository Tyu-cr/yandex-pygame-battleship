from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import QRect, QTimer
import sys
from random import randint
from game import Ui_Form


class Game(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_new_game.clicked.connect(self.new_game)
        self.btn_exit.clicked.connect(self.exit)
        self.setMouseTracking(True)

        self.x = 0
        self.y = 0
        self.text = ""
        self.pole = []
        self.comp_pole = []
        self.comp_turn_boolean = False
        # 0 - игра идет, 1 - победа игрока, 2 - победа компьютера
        self.end_game = 0

        # Загрузка изображений
        self.normal = QPixmap("img//1.png")
        self.partly = QPixmap("img//2.png")
        self.destroyed = QPixmap("img//3.png")
        self.bomb = QPixmap("img//4.png")

        # Таймер для обновления рисунков
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(50)

        self.new_game()

    # Кнопка новой игры
    def new_game(self):
        self.end_game = 0
        self.pole = []
        self.comp_pole = []
        self.make_list()
        self.make_ships()
        self.comp_pole = self.pole
        self.pole = []
        self.make_list()
        self.make_ships()

    # Кнопка выхода из игры
    def exit(self):
        sys.exit(app.exec_())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawCompField(qp)
        self.drawPlayerField(qp)
        self.drawText(qp)
        self.drawPole(qp)
        self.drawRedRect(qp)
        self.drawEnd(qp)
        qp.end()

    # Отрисовка сетки компьютера
    def drawCompField(self, qp):
        qp.setBrush(QColor(0, 0, 0))
        for i in range(11):
            qp.drawLine(100 + i * 30, 100, 100 + i * 30, 400)
            qp.drawLine(100, 100 + i * 30, 400, 100 + i * 30)

    # Отрисовка сетки игрока
    def drawPlayerField(self, qp):
        for i in range(11):
            qp.drawLine(500 + i * 30, 100, 500 + i * 30, 400)
            qp.drawLine(500, 100 + i * 30, 800, 100 + i * 30)

    # Отрисовка строк и столбцов
    def drawText(self, qp):
        qp.setFont(QFont("Decorative", 16))
        for i in range(1, 11):
            self.text = str(i)
            qp.drawText(73, 93 + i * 30, self.text)
            qp.drawText(473, 93 + i * 30, self.text)
            self.text = chr(ord("A") + i - 1)
            qp.drawText(78 + i * 30, 93, self.text)
            qp.drawText(478 + i * 30, 93, self.text)

    # Отрисока кораблей на полях
    def drawPole(self, qp):
        for i in range(10):
            for j in range(10):
                # Компьютер
                if self.comp_pole[i][j] != 0:
                    rect = QRect(100 + j * 30, 100 + i * 30, 30, 30)
                    # Ранен
                    if 8 <= self.comp_pole[i][j] <= 11:
                        qp.drawPixmap(rect, self.partly)
                    # Уничтожен
                    elif self.comp_pole[i][j] >= 15:
                        qp.drawPixmap(rect, self.destroyed)
                    # Выстрел
                    if self.comp_pole[i][j] >= 5:
                        qp.drawPixmap(rect, self.bomb)
                # Игрок
                if self.pole[i][j] != 0:
                    rect = QRect(500 + j * 30, 100 + i * 30, 30, 30)
                    # В норме
                    if 1 <= self.pole[i][j] <= 4:
                        qp.drawPixmap(rect, self.normal)
                    # Ранен
                    elif 8 <= self.pole[i][j] <= 11:
                        qp.drawPixmap(rect, self.partly)
                    # Уничтожен
                    elif self.pole[i][j] >= 15:
                        qp.drawPixmap(rect, self.destroyed)
                    # Выстрел
                    if self.pole[i][j] >= 5:
                        qp.drawPixmap(rect, self.bomb)

    # Отрисовка красных квадратов
    def drawRedRect(self, qp):
        x = self.x
        y = self.y
        qp.setBrush(QColor(200, 0, 0))
        if 400 >= x >= 100 and 400 >= y >= 100:
            if self.end_game == 0 and not self.comp_turn_boolean:
                i = (y - 100) // 30
                j = (x - 100) // 30
                if 0 <= i <= 9 and 0 <= j <= 9:
                    if self.comp_pole[i][j] <= 4:
                        qp.drawRect(100 + j * 30, 100 + i * 30, 30, 30)

    # Вывод информации о конце игры
    def drawEnd(self, qp):
        if self.end_game == 1:
            qp.setPen(QColor(0, 0, 0))
            qp.setFont(QFont("Decorative", 30))
            self.text = "Вы победили!!!"
            qp.drawText(320, 450, self.text)
        elif self.end_game == 2:
            qp.setPen(QColor(255, 0, 0))
            qp.setFont(QFont("Decorative", 30))
            self.text = "Вы проиграли..."
            qp.drawText(320, 450, self.text)

    # Создание массивов
    # 0 - пустая ячейка
    # 1 - однопалубный корабль
    # 2 - часть двухпалубного корабля
    # 3 - часть трёхпалубного корабля
    # 4 - часть четырёхпалубного корабля
    # -1 - ячейки вокруг целого корабля
    # -2 - ячейки воруг уничтоженного корабля или частично построенного
    # При выстреле к ячейке прибавляем 7
    # При полном уничтожении корабля добавляем к его частям ещё одну 7, а к ячейкам вокруг -1
    def make_list(self):
        for i in range(10):
            a = []
            for j in range(10):
                a.append(0)
            self.pole.append(a)

    # Проверка, что координаты лежат в списке
    def test_coords(self, i, j):
        if 0 <= i <= 9 and 0 <= j <= 9:
            return True
        else:
            return False

    # Проверка окончания игры
    def test_end(self):
        # 15 * 4 + 16 * 2 * 3 + 17 * 3 * 2 + 18 * 4
        num = 330
        k_comp = 0
        k_player = 0
        for i in range(10):
            for j in range(10):
                # Поиск уничтоженных
                if self.pole[i][j] >= 15:
                    k_player += self.pole[i][j]
                if self.comp_pole[i][j] >= 15:
                    k_comp += self.comp_pole[i][j]
        if k_player == num:
            self.end_game = 2
        elif k_comp == num:
            self.end_game = 1

    # Устанавливает значение val в ячейку
    def set_pole_value(self, i, j, val):
        if self.test_coords(i, j) and self.pole[i][j] == 0:
            self.pole[i][j] = val

    # Окружение ячейки значением val
    def surround(self, i, j, val):
        self.set_pole_value(i - 1, j - 1, val)
        self.set_pole_value(i - 1, j, val)
        self.set_pole_value(i - 1, j + 1, val)
        self.set_pole_value(i, j + 1, val)
        self.set_pole_value(i + 1, j + 1, val)
        self.set_pole_value(i + 1, j, val)
        self.set_pole_value(i + 1, j - 1, val)
        self.set_pole_value(i, j - 1, val)

    # После построения корабля заменяет -2 на -1
    def surround_end(self):
        for i in range(10):
            for j in range(10):
                if self.pole[i][j] == -2:
                    self.pole[i][j] = -1

    # Создание кораблей
    def make_ships(self):
        self.make_4(4)
        for i in range(2):
            self.make_4(3)
        for i in range(3):
            self.make_4(2)
        self.make_1()

    # Создание однопалубных кораблей
    def make_1(self):
        for _ in range(4):
            while True:
                i = randint(0, 9)
                j = randint(0, 9)
                if self.pole[i][j] == 0:
                    self.pole[i][j] = 1
                    self.surround(i, j, -1)
                    break

    # Создание многопалубных кораблей
    def make_4(self, kol):
        while True:
            flag = False
            i = randint(0, 9)
            j = randint(0, 9)
            if self.pole[i][j] == 0:
                direction = randint(0, 3)
                # Вверх
                if direction == 0:
                    if self.test_4(i - (kol - 1), j):
                        flag = True
                # Вправо
                elif direction == 1:
                    if self.test_4(i, j + (kol - 1)):
                        flag = True
                # Вниз
                elif direction == 2:
                    if self.test_4(i + (kol - 1), j):
                        flag = True
                # Влево
                elif direction == 3:
                    if self.test_4(i, j - (kol - 1)):
                        flag = True
                # Добавление ячеек кораблей
                if flag:
                    self.pole[i][j] = kol
                    self.surround(i, j, -2)
                    if direction == 0:
                        for k in range(1, kol):
                            self.pole[i - k][j] = kol
                            self.surround(i - k, j, -2)
                    elif direction == 1:
                        for k in range(1, kol):
                            self.pole[i][j + k] = kol
                            self.surround(i, j + k, -2)
                    elif direction == 2:
                        for k in range(1, kol):
                            self.pole[i + k][j] = kol
                            self.surround(i + k, j, -2)
                    elif direction == 3:
                        for k in range(1, kol):
                            self.pole[i][j - k] = kol
                            self.surround(i, j - k, -2)
                    self.surround_end()
                    break

    # Проверка, что возможно построить
    def test_4(self, i, j):
        if not self.test_coords(i, j):
            return False
        if self.pole[i][j] == 0 or self.pole[i][j] == -2:
            return True
        return False

    # Уменьшение значение ячейки на 1 после уничтожения
    def set_destroyed_pole_value(self, pole, i, j):
        if self.test_coords(i, j):
            if pole[i][j] == -1 or pole[i][j] == 6:
                pole[i][j] -= 1

    # Окружение клетки после уничтожения
    def surround_destroyed(self, pole, i, j):
        self.set_destroyed_pole_value(pole, i - 1, j - 1)
        self.set_destroyed_pole_value(pole, i - 1, j)
        self.set_destroyed_pole_value(pole, i - 1, j + 1)
        self.set_destroyed_pole_value(pole, i, j + 1)
        self.set_destroyed_pole_value(pole, i + 1, j + 1)
        self.set_destroyed_pole_value(pole, i + 1, j)
        self.set_destroyed_pole_value(pole, i + 1, j - 1)
        self.set_destroyed_pole_value(pole, i, j - 1)

    # Выстрел игрока при нажатии на кнопку мыши
    def shot(self, i, j):
        self.comp_pole[i][j] += 7
        self.test_destr(self.comp_pole, i, j)
        self.test_end()
        # Если промах
        if self.comp_pole[i][j] < 8:
            self.comp_turn_boolean = True
            while self.comp_turn_boolean:
                self.comp_turn_boolean = self.comp_turn()

    # Ход компьютера
    def comp_turn(self):
        flag_break = True
        flag_break_2 = True
        result = False
        flag = False
        # Ищет подбитый корабль
        for i in range(10):
            if flag_break:
                for j in range(10):
                    if 9 <= self.pole[i][j] <= 11:
                        flag = True
                        # Стреляет выше подбитого корабля
                        if self.test_coords(i - 1, j) and self.pole[i - 1][j] <= 4 and self.pole[i - 1][j] != -2:
                            self.pole[i - 1][j] += 7
                            self.test_destr(self.pole, i, j)
                            # Если попал в корабль
                            if self.pole[i - 1][j] >= 8:
                                result = True
                            flag_break = False
                            break
                        # Вниз
                        elif self.test_coords(i + 1, j) and self.pole[i + 1][j] <= 4 and self.pole[i + 1][j] != -2:
                            self.pole[i + 1][j] += 7
                            self.test_destr(self.pole, i, j)
                            if self.pole[i + 1][j] >= 8:
                                result = True
                            flag_break = False
                            break
                        # Влево
                        elif self.test_coords(i, j - 1) and self.pole[i][j - 1] <= 4 and self.pole[i][j - 1] != -2:
                            self.pole[i][j - 1] += 7
                            self.test_destr(self.pole, i, j)
                            if self.pole[i][j - 1] >= 8:
                                result = True
                            flag_break = False
                            break
                        # Вправо
                        elif self.test_coords(i, j + 1) and self.pole[i][j + 1] <= 4 and self.pole[i][j + 1] != -2:
                            self.pole[i][j + 1] += 7
                            self.test_destr(self.pole, i, j)
                            if self.pole[i][j + 1] >= 8:
                                result = True
                            flag_break = False
                            break
        # Если попадания не было или только уничтоженные
        if not flag:
            for k in range(100):
                i = randint(0, 9)
                j = randint(0, 9)
                if self.pole[i][j] <= 4 and self.pole[i][j] != -2:
                    self.pole[i][j] += 7
                    self.test_destr(self.pole, i, j)
                    if self.pole[i][j] >= 8:
                        result = True
                    flag = True
                    break
        # Если не нашёл за 100 попыток
        if not flag:
            for i in range(10):
                if flag_break_2:
                    for j in range(10):
                        if self.pole[i][j] <= 4 and self.pole != -2:
                            self.pole[i][j] += 7
                            self.test.destr(i, j)
                            if self.pole[i][j] >= 8:
                                result = True
                                flag_break_2 = False
                                break
        self.test_end()
        # True - попадание, False - промах
        return result

    # Проверка на уничтожение корабля
    def test_destr(self, pole, i, j):
        if pole[i][j] == 8:
            pole[i][j] += 7
            self.surround_destroyed(pole, i, j)
        elif pole[i][j] == 9:
            self.analise(pole, i, j, 2)
        elif pole[i][j] == 10:
            self.analise(pole, i, j, 3)
        elif pole[i][j] == 11:
            self.analise(pole, i, j, 4)

    def analise(self, pole, i, j, k):
        k_destroyed = 0
        # Считает кол-во уничтоженных частей корабля
        for i2 in range(i - (k - 1), i + k):
            for j2 in range(j - (k - 1), j + k):
                if self.test_coords(i2, j2) and pole[i2][j2] == k + 7:
                    k_destroyed += 1
        # Если уничтожен весь корабль
        if k == k_destroyed:
            for i2 in range(i - (k - 1), i + k):
                for j2 in range(j - (k - 1), j + k):
                    if self.test_coords(i2, j2) and pole[i2][j2] == k + 7:
                        pole[i2][j2] += 7
                        self.surround_destroyed(pole, i2, j2)

    # Получение координат мыши при её перемещении
    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.x = x
        self.y = y

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        self.x = x
        self.y = y
        # При нажатии кнопки мыши, если она в поле компьютера, происходит выстрел
        if 400 >= x >= 100 and 400 >= y >= 100:
            if self.end_game == 0 and not self.comp_turn_boolean:
                i = (y - 100) // 30
                j = (x - 100) // 30
                if 0 <= i <= 9 and 0 <= j <= 9:
                    if self.comp_pole[i][j] <= 4:
                        self.shot(i, j)


app = QApplication(sys.argv)
a = Game()
a.show()
sys.exit(app.exec_())

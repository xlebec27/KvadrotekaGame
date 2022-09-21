from PyQt5.Qt import *
import sys
import random


class Game(QMainWindow):
    def __init__(self, parent=None):
        super(Game, self).__init__(parent)

        self.level = 1
        self.initUI()
        self.createActions()
        self.initMenuBar()
        self.initGameData()

    def initUI(self):
        self.setWindowTitle("Kvadroteka")
        self.resize(700, 800)
        self.setFixedSize(self.width(), self.height())

    def initGameData(self):
        self.moveCount = 0
        self.spinCount = 0
        if self.level == 1:
            self.data = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]]
        elif self.level == 2:
            self.data = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]]
        elif self.level == 3:
            self.data = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [0, 0, 0, 0, 0]]
        elif self.level == 4:
            self.data = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [4, 4, 4, 4, 4]]
        else:
            self.data = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]]
        for n in range(random.randint(20, 30)):
            r = random.randint(0, 2)
            c = random.randint(0, 2)
            self.p1 = [r, c]
            self.p2 = [r + 2, c]
            self.p3 = [r + 2, c + 2]
            self.p4 = [r, c + 2]
            if random.choice([True, False]):
                self.rotateLeft()
            else:
                self.rotateRight()
        self.p1 = [1, 1]
        self.p2 = [3, 1]
        self.p3 = [3, 3]
        self.p4 = [1, 3]
        self.moveCount = 0
        self.spinCount = 0

    def newGameStart(self, l):
        self.level = l
        self.initGameData()
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawGameGraph(qp)
        qp.end()

    def createActions(self):
        self.level1Action = QAction(self)
        self.level1Action.setText("Level 1")
        self.level1Action.triggered.connect(lambda: self.newGameStart(1))
        self.level2Action = QAction(self)
        self.level2Action.setText("Level 2")
        self.level2Action.triggered.connect(lambda: self.newGameStart(2))
        self.level3Action = QAction(self)
        self.level3Action.setText("Level 3")
        self.level3Action.triggered.connect(lambda: self.newGameStart(3))
        self.level4Action = QAction(self)
        self.level4Action.setText("Level 4")
        self.level4Action.triggered.connect(lambda: self.newGameStart(4))

    def initMenuBar(self):
        self.statusBar()
        menubar = self.menuBar()
        levelmenu = menubar.addMenu('Level')
        levelmenu.addAction(self.level1Action)
        levelmenu.addAction(self.level2Action)
        levelmenu.addAction(self.level3Action)
        levelmenu.addAction(self.level4Action)

    def drawGameGraph(self, qp):
        self.drawTiles(qp)
        self.drawLabel(qp)

    def drawTiles(self, qp):
        for row in range(5):
            for column in range(5):
                color = self.data[row][column]
                if color == 0:
                    qp.setBrush(QColor(224, 175, 160))
                elif color == 1:
                    qp.setBrush(QColor(168, 212, 173))
                elif color == 2:
                    qp.setBrush(QColor(242, 247, 158))
                elif color == 3:
                    qp.setBrush(QColor(68, 55, 66))
                elif color == 4:
                    qp.setBrush(QColor(70, 129, 137))
                qp.drawRect(40 + column * 115, 165 + row * 115, 100, 100)
        qp.setPen(QPen(Qt.black, 6, Qt.SolidLine))
        pointx = 43 + self.p1[1] * 115
        pointy = 168 + self.p1[0] * 115
        qp.drawLine(pointx, pointy, pointx + 325, pointy)
        qp.drawLine(pointx + 325, pointy, pointx + 325, pointy + 325)
        qp.drawLine(pointx + 325, pointy + 325, pointx, pointy + 325)
        qp.drawLine(pointx, pointy + 325, pointx, pointy)

    @staticmethod
    def drawLabel(qp):
        qp.setFont(QFont("Verdana", 10, QFont.Light))
        qp.setPen(QColor(13, 10, 11))
        qp.drawText(20, 100, u"Выстройте квадраты одного цвета в один ряд. ")
        qp.drawText(20, 120, u"Управление: ")
        qp.drawText(20, 140, u"Используйте стрелки для перемещения указателя, \"z\" и \"x\" для вращения квадратов")
        qp.setFont(QFont("Verdana", 20, QFont.Light))
        qp.drawText(250, 60, "Квадротека")

    def keyPressEvent(self, e):
        keyCode = e.key()
        ret = False
        if keyCode == Qt.Key_Left:
            ret = self.move("Left")
        elif keyCode == Qt.Key_Right:
            ret = self.move("Right")
        elif keyCode == Qt.Key_Up:
            ret = self.move("Up")
        elif keyCode == Qt.Key_Down:
            ret = self.move("Down")
        elif keyCode == Qt.Key_Z:
            ret = self.move("Rotate Left")
        elif keyCode == Qt.Key_X:
            ret = self.move("Rotate Right")
        else:
            pass

        if ret:
            self.update()

    def move(self, direction):
        isMove = False
        if direction == "Left":
            isMove = self.moveLeft()
        elif direction == "Right":
            isMove = self.moveRight()
        elif direction == "Up":
            isMove = self.moveUp()
        elif direction == "Down":
            isMove = self.moveDown()
        elif direction == "Rotate Left":
            isMove = self.rotateLeft()
        elif direction == "Rotate Right":
            isMove = self.rotateRight()
        else:
            pass

        if not isMove:
            return False

        if self.isGameOver():
            button = QMessageBox.warning(self, "Предупреждение", u"Игра завершена",
                                         QMessageBox.Ok | QMessageBox.No,
                                         QMessageBox.Ok)
        else:
            return True

    def isGameOver(self):
        for n in range(5):
            curr_color = self.data[n][0]
            for i in self.data[n]:
                if i != curr_color:
                    return False
        return True

    def moveRight(self):
        if self.p3[1] < 4:
            self.p1[1] += 1
            self.p2[1] += 1
            self.p3[1] += 1
            self.p4[1] += 1
            self.moveCount += 1
            return True
        return False

    def moveLeft(self):
        if self.p1[1] > 0:
            self.p1[1] -= 1
            self.p2[1] -= 1
            self.p3[1] -= 1
            self.p4[1] -= 1
            self.moveCount += 1
            return True
        return False

    def moveUp(self):
        if self.p1[0] > 0:
            self.p1[0] -= 1
            self.p2[0] -= 1
            self.p3[0] -= 1
            self.p4[0] -= 1
            self.moveCount += 1
            return True
        return False

    def moveDown(self):
        if self.p3[0] < 4:
            self.p1[0] += 1
            self.p2[0] += 1
            self.p3[0] += 1
            self.p4[0] += 1
            self.moveCount += 1
            return True
        return False

    def rotateRight(self):
        temp = self.data[self.p1[0]][self.p1[1]]
        self.data[self.p1[0]][self.p1[1]] = self.data[self.p2[0]][self.p2[1]]
        self.data[self.p2[0]][self.p2[1]] = temp
        temp = self.data[self.p2[0]][self.p2[1]]
        self.data[self.p2[0]][self.p2[1]] = self.data[self.p3[0]][self.p3[1]]
        self.data[self.p3[0]][self.p3[1]] = temp
        temp = self.data[self.p3[0]][self.p3[1]]
        self.data[self.p3[0]][self.p3[1]] = self.data[self.p4[0]][self.p4[1]]
        self.data[self.p4[0]][self.p4[1]] = temp
        temp = self.data[self.p1[0] + 1][self.p1[1]]
        self.data[self.p1[0] + 1][self.p1[1]] = self.data[self.p2[0]][self.p2[1] + 1]
        self.data[self.p2[0]][self.p2[1] + 1] = temp
        temp = self.data[self.p2[0]][self.p2[1] + 1]
        self.data[self.p2[0]][self.p2[1] + 1] = self.data[self.p3[0] - 1][self.p3[1]]
        self.data[self.p3[0] - 1][self.p3[1]] = temp
        temp = self.data[self.p3[0] - 1][self.p3[1]]
        self.data[self.p3[0] - 1][self.p3[1]] = self.data[self.p4[0]][self.p4[1] - 1]
        self.data[self.p4[0]][self.p4[1] - 1] = temp
        self.spinCount += 1
        return True

    def rotateLeft(self):
        self.data[self.p3[0]][self.p3[1]], self.data[self.p4[0]][self.p4[1]] = self.data[self.p4[0]][self.p4[1]], \
                                                                               self.data[self.p3[0]][self.p3[1]]
        self.data[self.p2[0]][self.p2[1]], self.data[self.p3[0]][self.p3[1]] = self.data[self.p3[0]][self.p3[1]], \
                                                                               self.data[self.p2[0]][self.p2[1]]
        self.data[self.p1[0]][self.p1[1]], self.data[self.p2[0]][self.p2[1]] = self.data[self.p2[0]][self.p2[1]], \
                                                                               self.data[self.p1[0]][self.p1[1]]
        self.data[self.p3[0] - 1][self.p3[1]], self.data[self.p4[0]][self.p4[1] - 1] = self.data[self.p4[0]][
                                                                                           self.p4[1] - 1], \
                                                                                       self.data[self.p3[0] - 1][
                                                                                           self.p3[1]]
        self.data[self.p2[0]][self.p2[1] + 1], self.data[self.p3[0] - 1][self.p3[1]] = self.data[self.p3[0] - 1][
                                                                                           self.p3[1]], \
                                                                                       self.data[self.p2[0]][
                                                                                           self.p2[1] + 1]
        self.data[self.p1[0] + 1][self.p1[1]], self.data[self.p2[0]][self.p2[1] + 1] = self.data[self.p2[0]][
                                                                                           self.p2[1] + 1], \
                                                                                       self.data[self.p1[0] + 1][
                                                                                           self.p1[1]]
        self.spinCount += 1
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.exit(app.exec_())

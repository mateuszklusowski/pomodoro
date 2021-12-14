from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow,QApplication, QPushButton, QLabel
import sys
from math import floor


LABEL_STYLESHEET= ('background-color: #E8C5C9;' +
            'color: #100407;' +
            'font-size: 200px;'
            )
BTN_STYLESHEET = ('*{background-color: #100407;' +
            'color: #E8C5C9;' +
            'border-radius: 4px;'+
            'margin: 0px;' +
            'font-size: 20px;' +
            'padding: 4px;}' +
            '*:hover{background-color: #1F0A0E;}')
COUNTER = 0


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # window setting
        self.setWindowTitle("Pomodoro")
        self.setFixedHeight(500)
        self.setFixedWidth(800)
        self.setStyleSheet('background-color: #E8C5C9;')

        # work/break label
        self.upper_label = QLabel("test", self)
        self.upper_label.setFixedWidth(600)
        self.upper_label.setFixedHeight(50)
        self.upper_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.upper_label.setStyleSheet('background-color: #E8C5C9;' + 'color: #100407;' + 'font-size: 30px;')
        self.upper_label.move(100, -350)
        
        # label
        self.label = QLabel("00:00", self)
        self.label.setStyleSheet(LABEL_STYLESHEET)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedWidth(600)
        self.label.setFixedHeight(200)
        self.label.move(100, -300)
    
        # button
        self.button = QPushButton("START", self)
        self.button.setStyleSheet(BTN_STYLESHEET)
        self.button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.button.setFixedWidth(100)
        self.button.move(350, 400)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.start_timer)

        self.show()


    # animations
    def animation_down(self):
        if self.label.y() < 100:
            self.label.move(100, self.label.y() + 4)
            self.upper_label.move(100, self.upper_label.y() + 4)
            QtCore.QTimer.singleShot(6, lambda: self.animation_down())
            self.button.setDisabled(True)
        else:
            self.button.setEnabled(True)


    def animation_up(self):
        if self.label.y() > -300:
            self.label.move(100, self.label.y() - 4)
            self.upper_label.move(100, self.upper_label.y() - 4)
            QtCore.QTimer.singleShot(6, lambda: self.animation_up())
            self.button.setDisabled(True)
            self.upper_label.setText("")
        else:
            self.button.setEnabled(True)
        

    # counting down time
    def count_time(self, count):
        global COUNTER

        count_min = floor(count / 60)
        count_sec = count % 60

        if self.button.isChecked():
            
            self.button.setText("RESET")

            if count_sec < 10:
                self.label.setText(f"{count_min}:0{count_sec}")
            else:
                self.label.setText(f"{count_min}:{count_sec}")

            if count > 0:
                QtCore.QTimer.singleShot(1000, lambda: self.count_time(count - 1))
            else:
                self.start_timer()
        
        # reset timer
        else:
            COUNTER = 0
            self.animation_up()
            self.button.setText("START")
            return
        

    # start timer
    def start_timer(self):
        global COUNTER
 
        work_time = 25 * 60
        short_break_time = 5 * 60
        long_break_time = 20 * 60

        self.animation_down()

        if COUNTER < 8:
            if COUNTER % 2 == 0:
                self.upper_label.setText("work time")
                self.count_time(work_time)
                COUNTER +=1
            elif COUNTER % 2 != 0 and COUNTER != 7:
                self.upper_label.setText("break")
                self.count_time(short_break_time)
                COUNTER +=1
            else:
                self.upper_label.setText("long break")
                self.count_time(long_break_time)
                COUNTER +=1

        else:
            COUNTER = 0
            self.upper_label.setText("")
            self.label.setText(f"Done!")

      

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    sys.exit(app.exec())

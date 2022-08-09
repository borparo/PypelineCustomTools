"""
SIMPLE TIC TAC TOE GAME
A simple window tic tac toe game for 2 players.
:version: 0.1
:author: Borja Panadero
:year: 2021

TODO: Create custom QPushButton class with enum states
TODO: Create new algorithm for checking win combinations. Currently is hardcoded.
"""

from email.charset import QP
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPalette, QColor, QFont
import sys

class GameButton(QPushButton):
    def __init__(self, text):
        super(GameButton, self).__init__(text)
        btn_palette = self.palette
        btn_palette.setColor(QPalette.Button, QColor(Qt.darkCyan))
        btn_palette.setColor(QPalette.ButtonText, QColor(Qt.white))
        self.setPalette(self.dark())
        self.setFont(QFont("Arial", 16, QFont.Bold))


class SimpleTicTacToe(QDialog):
    def __init__(self):
        super(SimpleTicTacToe, self).__init__()
        self._player1_score = 0
        self._player2_score = 0
        self._current_player = 1
        self._buttons=[]

        self.setWindowTitle("Tic Tac Toe")
        self.setFixedWidth(240)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        title_font = QFont("Arial", 18, QFont.Bold)
        player_font = QFont('Arial', 12, QFont.Normal)
        score_font = QFont('Arial', 14, QFont.Black)
        button_font = QFont('Arial', 16, QFont.Black)

        self._title = QLabel("TIC TAC TOE")
        self._title.setFont(title_font)
        self._title.setAlignment(Qt.AlignCenter)

        self._player1_label = QLabel("Player 1:")
        self._player1_label.setAlignment(Qt.AlignLeft)
        self._player1_label.setFont(player_font)

        self._player2_label = QLabel("Player 2:")
        self._player2_label.setAlignment(Qt.AlignRight)
        self._player2_label.setFont(player_font)

        self._p1_score_label = QLabel(str(self._player1_score))
        self._p1_score_label.setAlignment(Qt.AlignCenter)
        self._p1_score_label.setFont(score_font)

        self._p2_score_label = QLabel(str(self._player2_score))
        self._p2_score_label.setAlignment(Qt.AlignCenter)
        self._p2_score_label.setFont(score_font)

        self._buttons = [QPushButton() for i in range(10)]
        for btn in self._buttons:
            btn.setFont(button_font)
        self._buttons_page = QWidget()

    def create_layouts(self):
        players_layout = QHBoxLayout()
        players_layout.addWidget(self._player1_label)
        players_layout.addWidget(self._p1_score_label)
        players_layout.addWidget(self._player2_label)
        players_layout.addWidget(self._p2_score_label)


        info_layout = QVBoxLayout()
        info_layout.addWidget(self._title)
        info_layout.addLayout(players_layout)
        info_layout.setSpacing(1)
        #info_layout.setAlignment(Qt.AlignCenter)

        buttons_grid = QGridLayout(self._buttons_page)
        buttons_grid.setContentsMargins(0, 0, 0, 0)
        buttons_grid.setSpacing(0)
        buttons_grid.setObjectName("buttons_grid")
        index = 0
        for row in range(3):
            for col in range(3):
                button = self._buttons[index]
                button.setMinimumHeight(65)
                button.setObjectName(str(index))
                buttons_grid.addWidget(button, row, col)
                index += 1

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self._buttons_page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

    def create_connections(self):
        for button in self._buttons:
            button.clicked.connect(self.set_button_sign)

    def set_button_sign(self):
        button = self.sender()
        #button.setFlat(True)
        palette = self.palette()
        
        print(type(button))
        if self._current_player == 1:
            palette.setColor(QPalette.Disabled,QPalette.Button, QColor(Qt.darkGreen))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(Qt.white))
            button.setForegroundRole(QPalette.Button)
            button.setAutoFillBackground(True)
            button.setPalette(palette)
            button.update()
            button.setText("X")
            #button.setStyleSheet("QPushButton {background-color:#33be75; color:white; font-size: 16pt; "
            #                     "font-weight:600;}")
            button.setEnabled(False)
            self._current_player = 2
        elif self._current_player == 2:
            
            palette.setColor(QPalette.Button, QColor(Qt.red))
            palette.setColor(QPalette.ButtonText, QColor(Qt.black))
            button.setForegroundRole(QPalette.Button)
            button.setAutoFillBackground(True)
            button.setPalette(palette)
            button.update()
            button.setText("O")
            #button.setStyleSheet("QPushButton {background-color:#982311; color:black; font-size: 16pt; "
            #                    "font-weight:600;}")
            button.setEnabled(False)
            self._current_player = 1
        self.check_for_win()

    def check_for_win(self):

        button0 = self.findChild(QPushButton,"0")
        button1 = self.findChild(QPushButton,"1")
        button2 = self.findChild(QPushButton,"2")
        button3 = self.findChild(QPushButton, "3")
        button4 = self.findChild(QPushButton, "4")
        button5 = self.findChild(QPushButton, "5")
        button6 = self.findChild(QPushButton, "6")
        button7 = self.findChild(QPushButton, "7")
        button8 = self.findChild(QPushButton, "8")

        # Top row case
        if button0.text() == "X"  and button1.text() == "X" and button2.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button0.text() == "O" and button1.text()  == "O" and button2.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # Mid row case
        if button3.text() == "X"  and button4.text() == "X" and button5.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button3.text() == "O" and button4.text()  == "O" and button5.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # Bottom row case
        if button6.text() == "X" and button7.text() == "X" and button8.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button6.text() == "O" and button7.text()  == "O" and button8.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # Lef col case
        if button0.text() == "X" and button3.text() == "X" and button6.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button0.text() == "O" and button3.text() == "O" and button6.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # Mid col case
        if button1.text() == "X" and button4.text() == "X" and button7.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button1.text() == "O" and button4.text() == "O" and button7.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # Right col case
        if button2.text() == "X" and button5.text() == "X" and button8.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button2.text() == "O" and button5.text() == "O" and button8.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # diagonal 1 col case
        if button0.text() == "X" and button4.text() == "X" and button8.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button0.text() == "O" and button4.text() == "O" and button8.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

        # diagonal 2 col case
        if button6.text() == "X" and button4.text() == "X" and button2.text() == "X":
            print("Player 1 wins!")
            self.freeze_board()
            self.update_score("player1")
            self.play_again()
        elif button6.text() == "O" and button4.text() == "O" and button2.text() == "O":
            print("Player 2 wins!")
            self.freeze_board()
            self.update_score("player2")
            self.play_again()

    def play_again(self):
        replay = QMessageBox(QMessageBox.Information,"Play again?", "Do you wanna play again?", QMessageBox.Yes | QMessageBox.No)
        answer = replay.exec_()
        if answer == replay.Yes:
            self.clean_board()

    def freeze_board(self):
        for button in self._buttons:
            if button.isEnabled():
                button.setEnabled(False)

    def update_score(self, player):
        if player == "player1":
            self._player1_score += 1
            self._p1_score_label.setText(str(self._player1_score))
        else:
            self._player2_score += 1
            self._p2_score_label.setText(str(self._player2_score))

    def clean_board(self):
        for button in self._buttons:
            button.setFlat(False)
            button.setText("")
            button.setEnabled(True)
            pal = QPalette()
            button.setAutoFillBackground(True)
            button.setPalette(pal)
            button.update()
            #button.setStyleSheet("QPushButton {background-color:; color:; font-size:; font-weight:;}")

    def dark(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase,
                            QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        return dark_palette


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleTicTacToe()
    #window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())








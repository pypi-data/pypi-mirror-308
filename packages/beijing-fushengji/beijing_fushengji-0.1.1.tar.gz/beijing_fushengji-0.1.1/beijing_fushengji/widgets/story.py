from PySide6 import QtCore, QtGui
from beijing_fushengji.app.tools import load
from pathlib import Path
from beijing_fushengji.widgets.styled_widget import StyledDialog

CURRENT = Path(__file__).resolve().parent


class StoryDlg(StyledDialog):
    start_sig: QtCore.Signal = QtCore.Signal(bool)

    def __init__(self, _parent=None, c_continue=False):
        super().__init__()

        self.ui = load("ui.story").Ui_Story()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/ICON/icon.ico"))

        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setStyleSheet(
            """
            QLabel, QPushButton, QTextBrowser, QGroupBox, QTextEdit, QRadioButton {{
                font: 12pt {family};
            }}
            """.format(family=family)
        )

        self.processHelpFile()

        self.ui.startGame.clicked.connect(self.start_game)
        self.ui.startGame.setEnabled(False)

        self.setWindowFlag(
            self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint
        )

        self.messages = [
            self.tr("Initialize hacker information...."),
            self.tr("Initialize the second loop information....."),
            self.tr("Initialize black market items..."),
            self.tr("Initialize random events..."),
            self.tr("Loading Beijing real-time news...."),
        ]
        self._count = 1

        if not c_continue:
            self.ui.statusText.setText(self.messages[0])
        else:
            self.ui.statusText.hide()

        if not c_continue:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_message)
            self.timer.setInterval(330)
            self.timer.start()
        else:
            self.ui.startGame.setEnabled(True)
            self.ui.startGame.setText(self.tr("Continue game >>"))
            self.ui.startGame.setFocus()
            self.ui.startGame.clicked.connect(self.start_game)

    def update_message(self):
        if self._count < 5:
            self.ui.statusText.setText(self.messages[self._count])
            self._count += 1
        else:
            self.timer.stop()
            QtCore.QTimer.singleShot(
                330,
                self.finish_init,
            )

    def finish_init(self):
        self.ui.statusText.setText(
            self.tr("The game has been initialized, ready to enter Beijing...")
        )
        self.ui.startGame.setEnabled(True)
        self.ui.startGame.setFocus()

    def processHelpFile(self):
        self.ui.statusText.setText(self.tr("Initialization help information...."))
        from beijing_fushengji.help_html import help

        self.help_file_encrypted = CURRENT.parent.joinpath("helpinfo")
        self.help_file: Path = self.help_file_encrypted.parent.joinpath("help.html")
        self.help_file.write_text(help, encoding="utf8")

    def remove_help_file(self):
        if self.help_file.exists():
            self.help_file.unlink()

    def start_game(self):
        self.start_sig.emit(True)
        self.close()

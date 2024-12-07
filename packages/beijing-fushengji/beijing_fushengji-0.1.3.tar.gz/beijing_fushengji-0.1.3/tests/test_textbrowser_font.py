from PySide6 import QtWidgets, QtGui
from pathlib import Path

import sys

CURRENT = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT.parent))
import beijing_fushengji.main_rc as main_rc


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.browser = QtWidgets.QTextEdit()
        self.browser.setText("我们是天上的星星")
        self.layout().addWidget(self.browser)
        self.setStyleSheet(
            """
            QLabel, QPushButton, QTextBrowser, QGroupBox, QTextEdit, QRadioButton {{
                font: 12pt {family};
            }}
            """.format(family=family)
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

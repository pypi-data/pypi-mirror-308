from PySide6 import QtCore, QtMultimedia
import sys
import beijing_fushengji.main_rc as main_rc  # noqa: F401


class X(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.effect = QtMultimedia.QSoundEffect()
        self.effect.setSource(QtCore.QUrl.fromLocalFile(":/SND/sound/vomit.wav"))
        self.effect.play()
        QtCore.QTimer.singleShot(1200, lambda: sys.exit())


if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)
    x = X()
    app.exec()

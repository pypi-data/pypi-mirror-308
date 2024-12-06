# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
import beijing_fushengji.main_rc as main_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1091, 678)
        self.new_game = QAction(MainWindow)
        self.new_game.setObjectName("new_game")
        self.top_players = QAction(MainWindow)
        self.top_players.setObjectName("top_players")
        self.settings = QAction(MainWindow)
        self.settings.setObjectName("settings")
        self.exit_game = QAction(MainWindow)
        self.exit_game.setObjectName("exit_game")
        self.bank = QAction(MainWindow)
        self.bank.setObjectName("bank")
        self.post_office = QAction(MainWindow)
        self.post_office.setObjectName("post_office")
        self.hospital = QAction(MainWindow)
        self.hospital.setObjectName("hospital")
        self.airport = QAction(MainWindow)
        self.airport.setObjectName("airport")
        self.rental_agency = QAction(MainWindow)
        self.rental_agency.setObjectName("rental_agency")
        self.cybercafe = QAction(MainWindow)
        self.cybercafe.setObjectName("cybercafe")
        self.beijing_intro = QAction(MainWindow)
        self.beijing_intro.setObjectName("beijing_intro")
        self.story = QAction(MainWindow)
        self.story.setObjectName("story")
        self.game_help = QAction(MainWindow)
        self.game_help.setObjectName("game_help")
        self.about = QAction(MainWindow)
        self.about.setObjectName("about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1091, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.new_game)
        self.menu.addAction(self.top_players)
        self.menu.addAction(self.settings)
        self.menu.addAction(self.exit_game)
        self.menu_2.addAction(self.bank)
        self.menu_2.addAction(self.post_office)
        self.menu_2.addAction(self.hospital)
        self.menu_2.addAction(self.airport)
        self.menu_2.addAction(self.rental_agency)
        self.menu_2.addAction(self.cybercafe)
        self.menu_3.addAction(self.beijing_intro)
        self.menu_3.addAction(self.story)
        self.menu_3.addAction(self.game_help)
        self.menu_3.addAction(self.about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Beijing Life", None)
        )
        self.new_game.setText(
            QCoreApplication.translate("MainWindow", "new game", None)
        )
        self.top_players.setText(
            QCoreApplication.translate("MainWindow", "Ranking", None)
        )
        self.settings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )
        self.exit_game.setText(QCoreApplication.translate("MainWindow", "exit", None))
        self.bank.setText(QCoreApplication.translate("MainWindow", "Bank", None))
        self.post_office.setText(
            QCoreApplication.translate("MainWindow", "Post Office", None)
        )
        self.hospital.setText(
            QCoreApplication.translate("MainWindow", "Hospital", None)
        )
        self.airport.setText(QCoreApplication.translate("MainWindow", "Airport", None))
        self.rental_agency.setText(
            QCoreApplication.translate("MainWindow", "Rental Agency", None)
        )
        self.cybercafe.setText(
            QCoreApplication.translate("MainWindow", "Cyber Cafe", None)
        )
        self.beijing_intro.setText(
            QCoreApplication.translate("MainWindow", "Beijing Intro", None)
        )
        self.story.setText(QCoreApplication.translate("MainWindow", "Game Story", None))
        self.game_help.setText(
            QCoreApplication.translate("MainWindow", "Game Guide", None)
        )
        self.about.setText(
            QCoreApplication.translate("MainWindow", "About this game", None)
        )
        self.menu.setTitle(QCoreApplication.translate("MainWindow", "System", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", "Places", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", "Help", None))

    # retranslateUi

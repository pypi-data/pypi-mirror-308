# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLCDNumber,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTableView,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
import beijing_fushengji.main_rc as main_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1005, 677)
        MainWindow.setStyleSheet(
            "QLabel, QPushButton, QTextBrowser, QAction, QMenu, QHeaderView, QStandardItem {\n"
            "                font: 12pt MiSans;\n"
            "}"
        )
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
        self.widget_14 = QWidget(self.centralwidget)
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_12 = QWidget(self.widget_14)
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_4 = QVBoxLayout(self.widget_12)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QLabel(self.widget_12)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.black_market = QTableView(self.widget_12)
        self.black_market.setObjectName("black_market")
        self.black_market.setStyleSheet(
            "QHeaderView, QStandardItem {\n" "                font: 12pt MiSans;\n" "}"
        )

        self.verticalLayout_4.addWidget(self.black_market)

        self.horizontalLayout_7.addWidget(self.widget_12)

        self.widget_8 = QWidget(self.widget_14)
        self.widget_8.setObjectName("widget_8")
        self.widget_8.setMinimumSize(QSize(120, 200))
        self.widget_8.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_2 = QVBoxLayout(self.widget_8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_8 = QLabel(self.widget_8)
        self.label_8.setObjectName("label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_8)

        self.buy = QPushButton(self.widget_8)
        self.buy.setObjectName("buy")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buy.sizePolicy().hasHeightForWidth())
        self.buy.setSizePolicy(sizePolicy)
        self.buy.setMaximumSize(QSize(16777215, 38))

        self.verticalLayout_2.addWidget(self.buy)

        self.label_9 = QLabel(self.widget_8)
        self.label_9.setObjectName("label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_9)

        self.sell = QPushButton(self.widget_8)
        self.sell.setObjectName("sell")
        sizePolicy.setHeightForWidth(self.sell.sizePolicy().hasHeightForWidth())
        self.sell.setSizePolicy(sizePolicy)
        self.sell.setMaximumSize(QSize(16777215, 38))

        self.verticalLayout_2.addWidget(self.sell)

        self.horizontalLayout_7.addWidget(self.widget_8)

        self.widget_13 = QWidget(self.widget_14)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_5 = QVBoxLayout(self.widget_13)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_7 = QLabel(self.widget_13)
        self.label_7.setObjectName("label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_7)

        self.my_room = QTableView(self.widget_13)
        self.my_room.setObjectName("my_room")
        self.my_room.setStyleSheet(
            "QHeaderView, QStandardItem {\n" "                font: 12pt MiSans;\n" "}"
        )

        self.verticalLayout_5.addWidget(self.my_room)

        self.horizontalLayout_7.addWidget(self.widget_13)

        self.verticalLayout_7.addWidget(self.widget_14)

        self.widget_15 = QWidget(self.centralwidget)
        self.widget_15.setObjectName("widget_15")
        self.widget_15.setStyleSheet(
            "QPushButton::disabled{\n" "	background-color: rgb(143, 240, 164);\n" "}"
        )
        self.horizontalLayout_8 = QHBoxLayout(self.widget_15)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox = QGroupBox(self.widget_15)
        self.groupBox.setObjectName("groupBox")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setMinimumSize(QSize(250, 191))
        self.groupBox.setStyleSheet("")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(5, -1, 5, 5)
        self.widget_3 = QWidget(self.groupBox)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget_4)
        self.label_2.setObjectName("label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.cash = QLCDNumber(self.widget_4)
        self.cash.setObjectName("cash")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cash.sizePolicy().hasHeightForWidth())
        self.cash.setSizePolicy(sizePolicy2)
        self.cash.setStyleSheet("color: rgb(87, 227, 137);")

        self.horizontalLayout_2.addWidget(self.cash)

        self.verticalLayout.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.saving = QLCDNumber(self.widget_5)
        self.saving.setObjectName("saving")
        sizePolicy2.setHeightForWidth(self.saving.sizePolicy().hasHeightForWidth())
        self.saving.setSizePolicy(sizePolicy2)
        self.saving.setStyleSheet("color: rgb(87, 227, 137);")

        self.horizontalLayout_4.addWidget(self.saving)

        self.verticalLayout.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_6)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.debt = QLCDNumber(self.widget_6)
        self.debt.setObjectName("debt")
        sizePolicy2.setHeightForWidth(self.debt.sizePolicy().hasHeightForWidth())
        self.debt.setSizePolicy(sizePolicy2)
        self.debt.setStyleSheet("color: rgb(240, 0, 0);")
        self.debt.setSmallDecimalPoint(False)
        self.debt.setDigitCount(5)
        self.debt.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        self.horizontalLayout_5.addWidget(self.debt)

        self.verticalLayout.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.widget_3)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_7)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.health = QLCDNumber(self.widget_7)
        self.health.setObjectName("health")
        sizePolicy2.setHeightForWidth(self.health.sizePolicy().hasHeightForWidth())
        self.health.setSizePolicy(sizePolicy2)
        self.health.setStyleSheet("color: rgb(87, 227, 137);")

        self.horizontalLayout_3.addWidget(self.health)

        self.label_6 = QLabel(self.widget_7)
        self.label_6.setObjectName("label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.fame = QLCDNumber(self.widget_7)
        self.fame.setObjectName("fame")
        sizePolicy2.setHeightForWidth(self.fame.sizePolicy().hasHeightForWidth())
        self.fame.setSizePolicy(sizePolicy2)
        self.fame.setStyleSheet("color: rgb(87, 227, 137);")

        self.horizontalLayout_3.addWidget(self.fame)

        self.verticalLayout.addWidget(self.widget_7)

        self.gridLayout.addWidget(self.widget_3, 0, 0, 1, 1)

        self.horizontalLayout_8.addWidget(self.groupBox)

        self.widget_10 = QWidget(self.widget_15)
        self.widget_10.setObjectName("widget_10")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy3)
        self.widget_10.setMinimumSize(QSize(160, 190))
        self.widget_10.setMaximumSize(QSize(300, 190))
        self.verticalLayout_3 = QVBoxLayout(self.widget_10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, 0, -1)
        self.switch_place = QPushButton(self.widget_10)
        self.switch_place.setObjectName("switch_place")
        sizePolicy.setHeightForWidth(self.switch_place.sizePolicy().hasHeightForWidth())
        self.switch_place.setSizePolicy(sizePolicy)
        self.switch_place.setMinimumSize(QSize(0, 0))
        self.switch_place.setStyleSheet("QPushButton{\n" "border: none;\n" "}")

        self.verticalLayout_3.addWidget(self.switch_place)

        self.widget_11 = QWidget(self.widget_10)
        self.widget_11.setObjectName("widget_11")
        self.widget_11.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_6 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 2)
        self.x1 = QPushButton(self.widget_11)
        self.x1.setObjectName("x1")
        sizePolicy.setHeightForWidth(self.x1.sizePolicy().hasHeightForWidth())
        self.x1.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.x1)

        self.x2 = QPushButton(self.widget_11)
        self.x2.setObjectName("x2")
        sizePolicy.setHeightForWidth(self.x2.sizePolicy().hasHeightForWidth())
        self.x2.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.x2)

        self.verticalLayout_3.addWidget(self.widget_11)

        self.switch_mode = QPushButton(self.widget_10)
        self.switch_mode.setObjectName("switch_mode")
        sizePolicy.setHeightForWidth(self.switch_mode.sizePolicy().hasHeightForWidth())
        self.switch_mode.setSizePolicy(sizePolicy)
        self.switch_mode.setStyleSheet("QPushButton{\n" "border: none;\n" "}")

        self.verticalLayout_3.addWidget(self.switch_mode)

        self.horizontalLayout_8.addWidget(self.widget_10)

        self.widget_9 = QWidget(self.widget_15)
        self.widget_9.setObjectName("widget_9")
        sizePolicy3.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy3)
        self.widget_9.setMinimumSize(QSize(261, 191))
        self.gridLayout_2 = QGridLayout(self.widget_9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.x8 = QPushButton(self.widget_9)
        self.x8.setObjectName("x8")
        sizePolicy.setHeightForWidth(self.x8.sizePolicy().hasHeightForWidth())
        self.x8.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x8, 2, 0, 1, 1)

        self.x5 = QPushButton(self.widget_9)
        self.x5.setObjectName("x5")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.x5.sizePolicy().hasHeightForWidth())
        self.x5.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.x5, 0, 2, 1, 1)

        self.x6 = QPushButton(self.widget_9)
        self.x6.setObjectName("x6")
        sizePolicy.setHeightForWidth(self.x6.sizePolicy().hasHeightForWidth())
        self.x6.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x6, 1, 0, 1, 1)

        self.x4 = QPushButton(self.widget_9)
        self.x4.setObjectName("x4")
        sizePolicy.setHeightForWidth(self.x4.sizePolicy().hasHeightForWidth())
        self.x4.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x4, 0, 1, 1, 1)

        self.x7 = QPushButton(self.widget_9)
        self.x7.setObjectName("x7")
        sizePolicy.setHeightForWidth(self.x7.sizePolicy().hasHeightForWidth())
        self.x7.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x7, 1, 2, 1, 1)

        self.x3 = QPushButton(self.widget_9)
        self.x3.setObjectName("x3")
        sizePolicy.setHeightForWidth(self.x3.sizePolicy().hasHeightForWidth())
        self.x3.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x3, 0, 0, 1, 1)

        self.x0 = QPushButton(self.widget_9)
        self.x0.setObjectName("x0")
        sizePolicy.setHeightForWidth(self.x0.sizePolicy().hasHeightForWidth())
        self.x0.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x0, 2, 2, 1, 1)

        self.x9 = QPushButton(self.widget_9)
        self.x9.setObjectName("x9")
        sizePolicy.setHeightForWidth(self.x9.sizePolicy().hasHeightForWidth())
        self.x9.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.x9, 2, 1, 1, 1)

        self.label_16 = QLabel(self.widget_9)
        self.label_16.setObjectName("label_16")
        self.label_16.setStyleSheet("image: url(:/bg/res/subway.bmp);")

        self.gridLayout_2.addWidget(self.label_16, 1, 1, 1, 1)

        self.horizontalLayout_8.addWidget(self.widget_9)

        self.verticalLayout_7.addWidget(self.widget_15)

        self.places = QWidget(self.centralwidget)
        self.places.setObjectName("places")
        self.places.setStyleSheet(
            "QPushButton {\n"
            "height: 40px;\n"
            "border: none;\n"
            "\n"
            "	background-color: rgb(192, 191, 188);\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "background-color: black;\n"
            "}"
        )
        self.horizontalLayout = QHBoxLayout(self.places)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.p_bank = QPushButton(self.places)
        self.p_bank.setObjectName("p_bank")
        sizePolicy.setHeightForWidth(self.p_bank.sizePolicy().hasHeightForWidth())
        self.p_bank.setSizePolicy(sizePolicy)
        self.p_bank.setStyleSheet(
            "QPushButton{\n"
            "icon: url(:/bg/res/bank.ico);\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "icon: url(:/bg/res/bank_hover.ico);\n"
            "}"
        )

        self.horizontalLayout.addWidget(self.p_bank)

        self.p_hospital = QPushButton(self.places)
        self.p_hospital.setObjectName("p_hospital")
        sizePolicy.setHeightForWidth(self.p_hospital.sizePolicy().hasHeightForWidth())
        self.p_hospital.setSizePolicy(sizePolicy)
        self.p_hospital.setStyleSheet(
            "QPushButton{\n"
            "icon: url(:/bg/res/hospital.ico);\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "icon: url(:/bg/res/hospital_hover.ico);\n"
            "}"
        )
        self.p_hospital.setFlat(False)

        self.horizontalLayout.addWidget(self.p_hospital)

        self.p_postoffice = QPushButton(self.places)
        self.p_postoffice.setObjectName("p_postoffice")
        sizePolicy.setHeightForWidth(self.p_postoffice.sizePolicy().hasHeightForWidth())
        self.p_postoffice.setSizePolicy(sizePolicy)
        self.p_postoffice.setStyleSheet(
            "QPushButton{\n"
            "icon: url(:/bg/res/postoffice.ico);\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "icon: url(:/bg/res/postoffice_hover.ico);\n"
            "}"
        )

        self.horizontalLayout.addWidget(self.p_postoffice)

        self.p_rent = QPushButton(self.places)
        self.p_rent.setObjectName("p_rent")
        sizePolicy.setHeightForWidth(self.p_rent.sizePolicy().hasHeightForWidth())
        self.p_rent.setSizePolicy(sizePolicy)
        self.p_rent.setStyleSheet(
            "QPushButton{\n"
            "icon: url(:/bg/res/rent.ico);\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "icon: url(:/bg/res/rent_hover.ico);\n"
            "}"
        )

        self.horizontalLayout.addWidget(self.p_rent)

        self.p_netcafe = QPushButton(self.places)
        self.p_netcafe.setObjectName("p_netcafe")
        sizePolicy.setHeightForWidth(self.p_netcafe.sizePolicy().hasHeightForWidth())
        self.p_netcafe.setSizePolicy(sizePolicy)
        self.p_netcafe.setStyleSheet(
            "QPushButton{\n"
            "icon: url(:/bg/res/netcafe.ico);\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "icon: url(:/bg/res/netcafe_hover.ico);\n"
            "}"
        )

        self.horizontalLayout.addWidget(self.p_netcafe)

        self.verticalLayout_7.addWidget(self.places)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 0, 9, 0)
        self.ticker = QTextBrowser(self.widget)
        self.ticker.setObjectName("ticker")
        sizePolicy5 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ticker.sizePolicy().hasHeightForWidth())
        self.ticker.setSizePolicy(sizePolicy5)
        self.ticker.setMaximumSize(QSize(16777215, 40))
        self.ticker.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(50, 180, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
            "color: white;"
        )
        self.ticker.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ticker.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ticker.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.verticalLayout_6.addWidget(self.ticker)

        self.verticalLayout_7.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1005, 33))
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
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Black Market", None)
        )
        self.label_8.setText(QCoreApplication.translate("MainWindow", "Buy", None))
        self.buy.setText(QCoreApplication.translate("MainWindow", "==>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", "Sell", None))
        self.sell.setText(QCoreApplication.translate("MainWindow", "<==", None))
        self.label_7.setText(
            QCoreApplication.translate("MainWindow", "Your rented house", None)
        )
        self.groupBox.setTitle(
            QCoreApplication.translate("MainWindow", "Your Status", None)
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Cash", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Savings", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", "Debt", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", "Health", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", "Fame", None))
        self.switch_place.setText(
            QCoreApplication.translate(
                "MainWindow", "I want to visit \n" "the capital", None
            )
        )
        self.x1.setText(QCoreApplication.translate("MainWindow", "Pingguoyuan", None))
        self.x2.setText(QCoreApplication.translate("MainWindow", "Gongzhufen", None))
        self.switch_mode.setText(
            QCoreApplication.translate("MainWindow", "Switch mode", None)
        )
        self.x8.setText(
            QCoreApplication.translate("MainWindow", "Changchun Street", None)
        )
        self.x5.setText(QCoreApplication.translate("MainWindow", "Dongzhimen", None))
        self.x6.setText(QCoreApplication.translate("MainWindow", "Fuxingmen", None))
        self.x4.setText(QCoreApplication.translate("MainWindow", "Jishuitan", None))
        self.x7.setText(QCoreApplication.translate("MainWindow", "Jianguomen", None))
        self.x3.setText(QCoreApplication.translate("MainWindow", "Xizhimen", None))
        self.x0.setText(
            QCoreApplication.translate(
                "MainWindow", "Beijing Railway \n" "Station", None
            )
        )
        self.x9.setText(QCoreApplication.translate("MainWindow", "Chongwenmen", None))
        self.label_16.setText("")
        self.p_bank.setText(QCoreApplication.translate("MainWindow", "Bank", None))
        self.p_hospital.setText(
            QCoreApplication.translate("MainWindow", "Hospital", None)
        )
        self.p_postoffice.setText(
            QCoreApplication.translate("MainWindow", "Post Office", None)
        )
        self.p_rent.setText(
            QCoreApplication.translate("MainWindow", "Rental agency", None)
        )
        self.p_netcafe.setText(
            QCoreApplication.translate("MainWindow", "Cyber Cafe", None)
        )
        self.ticker.setHtml(
            QCoreApplication.translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'MiSans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Sans\'; font-size:10pt;">Beijing News: Citizens reported that someone was selling counterfeit wine at the subway entrance | 12:09 | Guoly Computing company was established | 12:20 | Beijing issued management regulations for the online antiques market | 21:8.10 | Guoly Computing company launched &quot;Beijing Fushengji&quot; survival strategy Games | 13:10 | Guoly Computing s'
                "eeks venture capital (guoxh@hotmail.com) | 2:25.00 | Chengdu smuggled plane successfully bids for Beijingers | 2:45.50 | Capital agency: big predictions for Beijing property market next year | 3:55.00 | The auto industry is once again aggressively recruiting Beijing Automobile to pay a thousand-yuan adjustment | 13:6.25 | North Korea supports Beijing's bid to host the Olympics | 2:35 | Famous painter An Qianlei: A promise between Beijing and me | 8:28.30 | Discounted air tickets for 50 yuan You can fly from Beijing East to Changping | 16:2.30 | Beijing combines the ban on setting off fireworks and firecrackers with the love for animals | 13:35.00 | Beijing Computer Sports Lottery announced that the 1.2 billion grand prize was claimed by a man | 7:06.00 | Xicheng's &quot;anti-pornography&quot; The regular army takes action &quot;quickly, accurately and ruthlessly&quot; | 4:62.00 | Beijing police crack down on those who buy and sell fake cosmetics | 10:60.00 | Witnesses in Beijing: Vendors are rampant at subway "
                "entrances, and people say the relevant departments should take control | 2:19.50 | Imported toys and electronics Business website (ePlayMe.com) launched in Beijing | 20:1.80 | 200,000 teachers and students in the capital signed in support of the Olympic bid | 23:1.00 | &quot;Beijing Pravda&quot; recruitment reporters will undergo re-examination on Saturday | 5:04.15 | Thousand-year-old wine appears in Beijing The fragrance of counterfeit wine is the best | 9:16.00 | High-tech development in rural areas: VCD sellers gather in the capital | 4:00.00 | Seven major trends in parallel-imported mobile phones in Beijing attract scientists' attention | 7:12:5 | Beijing's environmentally friendly toilets enter the United States | 23 :50 (US Western Time) | Three ears were cut off after a fellow villager turned against him | 5:40 | Police raided in the early morning and seized 5,000 copies of &quot;It Looks Really Fake&quot; | 4:08 | Beijing's new fashion: Give away lottery tickets during the holidays | 19: 45 | College "
                "students working in Beijing proudly say: Our housing will be available for purchase in 100 years | 10:46 | Beijing has made great achievements in environmental protection, Shougang is more than 10 times more beautiful than the park | 7:13.00 | Citizen Uncle Zhang reflects that some people Selling &quot;Shanghai Baby&quot; at the subway entrance | 6:00 | The CEO of a company in Zhongguancun accidentally drank Shanxi fake liquor and passed out, and the date of entering NSDQ was postponed | 20:0.50 | &quot;Universal Qigong Daily&quot;: Registration for the crash course on sinking qi in Dantian has begun | 15 :50 | Public security in Beijing has reached a new level and it has been rated as the safest city in the world | 19:00.00 | Officials joked about why the phenomenon of arbitrary fees in Beijing disappeared | 20:00 | The Industry and Commerce Bureau investigated a pirated VCD den | 4:0:00 | American experts: Beijing\u2019s air contains a variety of minerals and is rich in nutrients | 8:15:00 (US Eastern Time) "
                "| An expensive car turned out to be a smuggled car in Xiamen | 8:59:00 | College graduate job fair information: University of Posts and Telecommunications The supply of students exceeds the demand, and many IT companies are snatching people | 4:16:00 | Primary school students from all over the world gather in Beijing to see white pollution and sandstorms | 6:20:00 (Paris time) | Letter of thanks from Swan Lake: Beijingers saved wild swans | 6:18:00 | At the Hong Kong conference, Beijing was rated as the cleanest city | 6:48:00 | A good district chief who insists on &quot;putting relatives second and talents first&quot; | 2:32:85 | Experts say: FoxLoveChicken.com website will not go bankrupt and will be profitable in 2 years | 3:30 | Leaders say: Beijing\u2019s roads are in good condition | 4:07 | Citizens complain about too many fake medical advertisements in Beijing newspapers | 5:53 | Chen Gou Miss Cat's &quot;I Love Beijing's Hutongs&quot; won the first place in the essay competition | 4:40 | Community resi"
                "dents warned thieves: Stop stealing bicycles | 10:85 | A police station in Beijing was accused of moving someone else's household registration without permission | 4:00 | Beijing A university adheres to the lifelong system of &quot;doctoral supervisors&quot; and is praised by American professors | 19:09 | The 150th issue of the Beijing Sports Lottery draws a special prize of 20,000 first prize | 5:63 | Archaeological excavation of &quot;Yak Hutong&quot; in Beijing , the live TV broadcast turned into a farce | 10:09 | Restaurants and other service industries will extend their business hours during Teachers\u2019 Day in Beijing | 23:00 | Three hundred buildings in Beijing have achieved broadband access | 3:40 | Beijing public security improves the order of passenger transportation during the festival | 8:23 | There are millions of college students &quot;working&quot; in Zhongguancun | 2:00 | Our city's polluting enterprises have decreased by 12% compared with the previous year | 11:34 | The securities market has"
                " achieved a new breakthrough and annual financing has exceeded the trillion mark for the first time | 20:40 | Today End of news, replay in one minute | 14:24</span></p></body></html>",
                None,
            )
        )
        self.menu.setTitle(QCoreApplication.translate("MainWindow", "System", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", "Places", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", "Help", None))

    # retranslateUi

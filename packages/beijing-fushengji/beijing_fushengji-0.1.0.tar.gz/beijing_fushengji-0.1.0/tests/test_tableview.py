import PySide6.QtWidgets as QtWidgets
import PySide6.QtGui as QtGui

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.table_view = QtWidgets.QTableView()
        self.model = QtGui.QStandardItemModel()
        self.table_view.setModel(self.model)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table_view)

        self.add_item_with_icon()

    def add_item_with_icon(self):
        icon = QtGui.QIcon("res/bank.ico")  # Replace with your icon path

        item = QtGui.QStandardItem("Item Text")
        item.setIcon(icon)

        self.model.appendRow(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
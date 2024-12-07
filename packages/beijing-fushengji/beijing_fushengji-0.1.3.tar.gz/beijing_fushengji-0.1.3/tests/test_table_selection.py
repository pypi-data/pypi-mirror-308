import sys
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex):
        return len(self._data)

    def columnCount(self, parent: QModelIndex):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        data = [["Alice", 25], ["Bob", 30], ["Charlie", 35]]

        self.model = TableModel(data)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.setCentralWidget(self.table_view)

        self.table_view.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )

    def on_selection_changed(self, selected, deselected):
        if len(selected.indexes()) == 0:
            print("no row selected")
        for index in selected.indexes():
            row = index.row()
            print(f"Row {row} selected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog

from package.DataBase.CardDB import CardDB
from package.ui.SearchUI import Ui_SearchWindow
from package.ui.AddCardDialog import Ui_AddCardDialog


class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        from package.DataBase.config import config
        super(SearchWindow, self).__init__()
        self.ui = Ui_SearchWindow()
        self.ui.setupUi(self)
        self.ui.searchButton.clicked.connect(self.search_clicked)
        self.t = QtWidgets.QAction()
        self.ui.actionAddCard.triggered.connect(self.add_card_window)

        path = os.path.abspath("../DataBase/database.ini")
        config = config(path)
        self.card_db = CardDB(config)

    def add_card_window(self):
        # widget = AddCardWindow()
        try:
            widget = AddCardDialog(self.card_db)
            widget.show()
            widget.exec_()
        except (Exception) as err:
            print("Error")
            print(err)

    def search_clicked(self):
        card_name = self.ui.cardInput.text()
        results = self.card_db.get_card_info_by_name(card_name)
        if type(results) is list and results:
            self.ui.resultTable.setRowCount(len(results))
            self.ui.resultTable.setColumnCount(len(results[0]))

            for i, arg in enumerate(results):
                for j, key in enumerate(arg):
                    val = str(arg[key])
                    self.ui.resultTable.setItem(i, j, QtWidgets.QTableWidgetItem(val))
            # self.ui.CardResult.move(0, 0)


class AddCardDialog(QtWidgets.QDialog):

    def __init__(self, cardDB):
        super(AddCardDialog, self).__init__()
        self.ui = Ui_AddCardDialog()
        self.ui.setupUi(self)
        # Database
        self.cardDB = cardDB

        # Actions
        self.ui.okButton.clicked.connect(self.add_card)

    def add_card(self):
        card_name =
        std_checked = self.ui.stdCheckBox.isChecked()
        modern_checked = self.ui.modernCheckBox.isChecked()
        proxy_checked = self.ui.proxyCheckBox.isChecked()
        foil_checked = self.ui.foilCheckBox.isChecked()


app = QtWidgets.QApplication([])

application = SearchWindow()

application.show()

sys.exit(app.exec())
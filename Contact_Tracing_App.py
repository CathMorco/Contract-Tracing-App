from PyQt5 import QtWidgets


class GUI:
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Contact Tracing")

        # Create the buttons
        self.button1 = QtWidgets.QPushButton("Add Entry")
        self.button1.clicked.connect(self.Add_Entry)

        self.button2 = QtWidgets.QPushButton("Search Entry")
        self.button2.clicked.connect(self.Search_Entry)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.window.setLayout(layout)
        self.window.setGeometry(100, 100, 600, 400)





    def main(self):
        self.window.show()
        self.app.exec_()

    def Add_Entry(self):
        # Clear the current GUI
        while self.window.layout().count():
            item = self.window.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.button1 = QtWidgets.QPushButton("Go Back")
        self.button1.clicked.connect(self.go_back_option)
        self.window.layout().addWidget(self.button1)


    def Search_Entry(self):
        # Clear the current GUI
        while self.window.layout().count():
            item = self.window.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.button1 = QtWidgets.QPushButton("Go Back")
        self.button1.clicked.connect(self.go_back_option)
        self.window.layout().addWidget(self.button1)

    def go_back_option(self):
        while self.window.layout().count():
            item = self.window.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.button1 = QtWidgets.QPushButton("Add Entry")
        self.button1.clicked.connect(self.Add_Entry)
        self.window.layout().addWidget(self.button1)

        self.button2 = QtWidgets.QPushButton("Search Entry")
        self.button2.clicked.connect(self.Search_Entry)
        self.window.layout().addWidget(self.button2)


if __name__ == '__main__':
    window = GUI()
    window.main()
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QStackedWidget, QLabel, QLineEdit


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Contact Tracing")

        self.stacked_widget = QStackedWidget()

        # Add Entry View
        self.addEntryWidget = QtWidgets.QWidget()
        self.name_label = QLabel("Name:", self.addEntryWidget)
        self.name_input = QLineEdit(self.addEntryWidget)

        self.age_label = QLabel("Age:", self.addEntryWidget)
        self.age_input = QLineEdit(self.addEntryWidget)

        self.address_label = QLabel("Address:", self.addEntryWidget)
        self.address_input = QLineEdit(self.addEntryWidget)

        self.contact_label = QLabel("Contact Number:", self.addEntryWidget)
        self.contact_input = QLineEdit(self.addEntryWidget)
        self.save_button = QtWidgets.QPushButton("Save", self.addEntryWidget)
        self.save_button.clicked.connect(self.save_text_to_file)
        add_entry_layout = QtWidgets.QFormLayout(self.addEntryWidget)
        add_entry_layout.addRow(self.name_label, self.name_input)
        add_entry_layout.addRow(self.age_label, self.age_input)
        add_entry_layout.addRow(self.address_label, self.address_input)
        add_entry_layout.addRow(self.contact_label, self.contact_input)
        add_entry_layout.addWidget(self.save_button)

        # Search Entry View
        self.searchEntryWidget = QtWidgets.QWidget()
        search_entry_label = QtWidgets.QLabel("Search Entry View", self.searchEntryWidget)
        search_entry_layout = QtWidgets.QVBoxLayout(self.searchEntryWidget)
        search_entry_layout.addWidget(search_entry_label)

        # Add both views to the stacked widget
        self.stacked_widget.addWidget(self.addEntryWidget)
        self.stacked_widget.addWidget(self.searchEntryWidget)

        # Create the buttons
        self.addEntryButton = QtWidgets.QPushButton("Add Entry")
        self.addEntryButton.clicked.connect(self.show_add_entry_view)

        self.searchEntryButton = QtWidgets.QPushButton("Search Entry")
        self.searchEntryButton.clicked.connect(self.show_search_entry_view)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.addEntryButton)
        layout.addWidget(self.searchEntryButton)
        layout.addWidget(self.stacked_widget)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 600, 400)

    def main(self):
        self.window.show()
        self.app.exec_()

    def show_add_entry_view(self):
        self.stacked_widget.setCurrentWidget(self.addEntryWidget)

    def show_search_entry_view(self):
        self.stacked_widget.setCurrentWidget(self.searchEntryWidget)

    def save_text_to_file(self):
        text = self.text_edit.toPlainText()
        if text.strip() == "":
            QMessageBox.warning(self, "Warning", "Cannot save an empty text!")
            return

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text)
                QMessageBox.information(self, "Success", "Text saved to file successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the text: {e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = GUI()
    window.show()
    app.exec_()
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QStackedWidget, QLabel, QLineEdit, QCompleter, QFormLayout


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Contact Tracing")

        self.stacked_widget = QStackedWidget()

        # Add Entry View
        self.addEntryWidget = QtWidgets.QWidget()

        # auto complete options                                                 
        places = ["PUP Main - A. Mabini Campus, Sta. Mesa, Manila","PUP College of Engineering and Architecture Bldg., NDC Compound Anonas cor Pureza Sts., Sta. Mesa, Manila 1016", "College of Communication, COC Building, NDC Compound, Anonas St., Sta. Mesa, Manila 1016","PUP Institute of Technology, NDC Compound, Pureza St., Sta. Mesa, Manila, Philippines 1016", "PUP University Center for Culture and the Arts, Sentrong Pang-unibersidad para sa Kultura at mga Sining,  College of Communication Compound, NDC Campus, Anonas St. Sta. Mesa, Manila 1016"]
        self.completer = QCompleter(places)

        # create line edit and add auto complete                                
        self.places_label = QLabel("Last Place Visited:", self.addEntryWidget)
        self.places_input = QLineEdit(self.addEntryWidget)
        self.places_input.setCompleter(self.completer)


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
        add_entry_layout.addRow(self.places_label, self.places_input)
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
        name = self.name_input.text()
        age = self.age_input.text()
        address = self.address_input.text()
        contact_number = self.contact_input.text()

        if not name.strip() or not age.strip() or not address.strip() or not contact_number.strip():
            QMessageBox.warning(self, "Warning", "All fields must be filled!")
            return

        new_place = self.places_input.text().strip()
        if new_place:
            places_list = self.completer.model().stringList()
            places_list.append(new_place)
            self.completer.setModel(QtCore.QStringListModel(places_list))
            self.places_input.setCompleter(self.completer)

        file_name = "".join(c if c.isalnum() else "_" for c in name)

        # Set the file path including the name
        file_path = os.path.join("C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/TextFiles", f"{file_name}.txt")
        try:
            with open(file_path, "w") as file:
                file.write("Name: " + name + "\n")
                file.write("Age: " + age + "\n")
                file.write("Address: " + address + "\n")
                file.write("Contact Number: " + contact_number + "\n")
                file.write("Last Place Visited: " + new_place + "\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the text: {e}")


        QMessageBox.information(self, "Success", "Data saved successfully!")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = GUI()
    window.show()
    app.exec_()
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QStackedWidget, QLabel, QLineEdit, QCompleter, QFormLayout, QTextEdit
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt



class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Contact Tracing")

        self.stacked_widget = QStackedWidget()

        # Add Entry View
        self.addEntryWidget = QtWidgets.QWidget()

        # auto complete options for places in Add Entry
        places = self.load_places_from_file()                                                 
        self.completer = QCompleter(places)
        self.completer.setCaseSensitivity(0)

        # auto complete options for Entries in Search Entry
        searchEntry = self.load_entries_from_folder()                                                 
        self.completer2 = QCompleter(searchEntry)
        self.completer2.setCaseSensitivity(0)

        # create line edit and add auto complete                                
        self.places_label = QLabel("Last Place Visited Today:", self.addEntryWidget)
        self.places_input = QLineEdit(self.addEntryWidget)
        self.places_input.setCompleter(self.completer)
        

        #User Name Input in addEntryWidget
        self.name_label = QLabel("Name:", self.addEntryWidget)
        self.name_input = QLineEdit(self.addEntryWidget)

        #User Age Input in addEntryWidget
        self.age_label = QLabel("Age:", self.addEntryWidget)
        self.age_input = QLineEdit(self.addEntryWidget)

        #User Address Input in addEntryWidget
        self.address_label = QLabel("Address:", self.addEntryWidget)
        self.address_input = QLineEdit(self.addEntryWidget)

        #User Contact Number Input in addEntryWidget
        self.contact_label = QLabel("Contact Number:", self.addEntryWidget)
        self.contact_input = QLineEdit(self.addEntryWidget)

        #Creating Save Button
        self.save_button = QtWidgets.QPushButton("Save", self.addEntryWidget)
        self.save_button.clicked.connect(self.save_text_to_file)

        #Form Layout of addEntryWidget
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

        # create line edit and add auto complete for searchEntry
        self.search_input_label = QLabel("Search Text:", self.searchEntryWidget)
        self.search_input = QLineEdit(self.searchEntryWidget)
        self.search_input.setCompleter(self.completer2)

        self.file_content_text_edit = QTextEdit(self.searchEntryWidget)
        self.file_content_text_edit.setReadOnly(True)
        search_entry_layout.addWidget(self.search_input_label)
        search_entry_layout.addWidget(self.search_input)
        search_entry_layout.addWidget(self.file_content_text_edit)

        # Add both views to the stacked widget
        self.stacked_widget.addWidget(self.addEntryWidget)
        self.stacked_widget.addWidget(self.searchEntryWidget)

        # Create the Add Entry and Search Entry buttons
        self.addEntryButton = QtWidgets.QPushButton("Add Entry")
        self.addEntryButton.clicked.connect(self.show_add_entry_view)

        self.searchEntryButton = QtWidgets.QPushButton("Search Entry")
        self.searchEntryButton.clicked.connect(self.show_search_entry_view)

        #Layout of the program
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.addEntryButton)
        layout.addWidget(self.searchEntryButton)
        layout.addWidget(self.stacked_widget)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 600, 400)

        self.completer2.activated.connect(self.display_file_content)

        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #333333;
            }
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #7393B3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0096FF;
            }
        """)

    def main(self):
        self.window.show()
        self.app.exec_()

    def show_add_entry_view(self):
        self.stacked_widget.setCurrentWidget(self.addEntryWidget)

    def show_search_entry_view(self):
        self.stacked_widget.setCurrentWidget(self.searchEntryWidget)

    # Loads entries from the folder
    def load_entries_from_folder(self):
        folder_path = "C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/TextFiles"
        if os.path.exists(folder_path):
            try:
                file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                return file_names
            except Exception as e:
                print(f"An error occurred while loading files from the folder: {e}")
        return []

    def display_file_content(self, selected_file):
        if not selected_file.strip():
            QMessageBox.warning(self, "Warning", "Please enter a valid file name!")
            return

        folder_path = "C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/TextFiles"
        file_path = os.path.join(folder_path, selected_file)

        try:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.file_content_text_edit.setPlainText(file_content)
        except Exception as e:
            self.file_content_text_edit.setPlainText(f"An error occurred while reading the file: {e}")




    # Loads places from the file
    def load_places_from_file(self):
        file_path = "C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/PlacesList/places.txt"
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    places_list = [line.strip() for line in file.readlines()]
                return places_list
            except Exception as e:
                print(f"An error occurred while loading places from the file: {e}")
        return None

    # Saves places to the file
    def save_places_to_file(self, places_list):
        file_path = "C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/PlacesList/places.txt"
        try:
            with open(file_path, "w") as file:
                file.write("\n".join(places_list))
        except Exception as e:
            print(f"An error occurred while saving places to the file: {e}")


    #Saves the user's input into a text file
    def save_text_to_file(self):
        name = self.name_input.text()
        age = self.age_input.text()
        address = self.address_input.text()
        contact_number = self.contact_input.text()
        place = self.places_input.text()
        now = QDate.currentDate()

        #Requires the user to fill in all fields
        if not name.strip() or not age.strip() or not address.strip() or not contact_number.strip():
            QMessageBox.warning(self, "Warning", "All fields must be filled!")
            return

        file_name = "".join(c if c.isalnum() else "_" for c in name)


        # Add new place to the places list
        new_place = place.strip()
        if new_place:
            places_list = self.completer.model().stringList()
            if new_place not in places_list:
                places_list = self.completer.model().stringList()
                places_list.append(new_place)
                self.completer.setModel(QtCore.QStringListModel(places_list))
                self.places_input.setCompleter(self.completer)
                # Save the updated places list to the file
                self.save_places_to_file(places_list)

        # Set the file path including the name
        file_path = os.path.join("C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/TextFiles", f"{file_name}.txt")
        try:
            with open(file_path, "w") as file:
                file.write("Name: " + name + "\n")
                file.write("Age: " + age + "\n")
                file.write("Address: " + address + "\n")
                file.write("Contact Number: " + contact_number + "\n")
                file.write("Last Place Visited: " + place + "\n")
                file.write("Date: " +  now.toString(Qt.ISODate) + "\n")
            QMessageBox.information(self, "Success", "Data saved successfully!")

            self.name_input.clear()
            self.age_input.clear()
            self.address_input.clear()
            self.contact_input.clear()
            self.places_input.clear()

            searchEntry = self.load_entries_from_folder()
            self.completer2.setModel(QtCore.QStringListModel(searchEntry))
            self.search_input.setCompleter(self.completer2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the text: {e}")





        

#Runs the main program
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = GUI()
    window.show()
    app.exec_()
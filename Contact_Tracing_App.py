import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QStackedWidget, QLabel, QLineEdit, QCompleter, QTextEdit, QPushButton, QRadioButton, QButtonGroup
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
import re



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
        self.age_input.setValidator(QIntValidator(0, 150, self))

        #User Address Input in addEntryWidget
        self.address_label = QLabel("Address:", self.addEntryWidget)
        self.address_input = QLineEdit(self.addEntryWidget)

        #User Contact Number Input in addEntryWidget
        self.contact_label = QLabel("Contact Number:", self.addEntryWidget)
        self.contact_input = QLineEdit(self.addEntryWidget)
        contact_validator = QRegExpValidator(QRegExp(r'\d+'), self) 
        self.contact_input.setValidator(contact_validator)

        #Creating Save Button
        self.save_button = QtWidgets.QPushButton("Save", self.addEntryWidget)
        self.save_button.clicked.connect(self.save_text_to_file)


        # Creating the radio buttons for Covid-19 testing
        self.covid_label = QLabel("Have you been tested for Covid-19 in the last 14 days?", self.addEntryWidget)
        self.covid_no_button = QRadioButton("No", self.addEntryWidget)
        self.covid_pending_button = QRadioButton("Yes - Pending", self.addEntryWidget)
        self.covid_negative_button = QRadioButton("Yes - Negative", self.addEntryWidget)
        self.covid_positive_button = QRadioButton("Yes - Positive", self.addEntryWidget)
        #Invisible radio buttons so that the radio buttons can be "cleared" after saving a new entry
        self.dummy_radio_button = QRadioButton(self.addEntryWidget)
        self.dummy_radio_button.setVisible(False)


        # Creating a button group for the radio buttons to make them mutually exclusive
        self.covid_button_group = QButtonGroup(self.addEntryWidget)
        self.covid_button_group.addButton(self.covid_no_button)
        self.covid_button_group.addButton(self.covid_pending_button)
        self.covid_button_group.addButton(self.covid_negative_button)
        self.covid_button_group.addButton(self.covid_positive_button)
        self.covid_button_group.addButton(self.dummy_radio_button)
        #Form Layout of addEntryWidget
        add_entry_layout = QtWidgets.QFormLayout(self.addEntryWidget)
        add_entry_layout.addRow(self.places_label, self.places_input)
        add_entry_layout.addRow(self.name_label, self.name_input)
        add_entry_layout.addRow(self.age_label, self.age_input)
        add_entry_layout.addRow(self.address_label, self.address_input)
        add_entry_layout.addRow(self.contact_label, self.contact_input)
        add_entry_layout.addRow(self.covid_label)
        add_entry_layout.addRow(self.covid_no_button)
        add_entry_layout.addRow(self.covid_pending_button)
        add_entry_layout.addRow(self.covid_negative_button)
        add_entry_layout.addRow(self.covid_positive_button)
        add_entry_layout.addWidget(self.save_button)




        # Search Entry View
        self.searchEntryWidget = QtWidgets.QWidget()
        search_entry_label = QtWidgets.QLabel("Search Entry View", self.searchEntryWidget)
        search_entry_layout = QtWidgets.QVBoxLayout(self.searchEntryWidget)
        search_entry_layout.addWidget(search_entry_label)
        self.positive_count_label = QLabel(self.searchEntryWidget)
        self.search_positive_button = QPushButton("Search Positive Cases", self.searchEntryWidget)
        self.search_positive_button.clicked.connect(self.search_positive_cases)

        # create line edit and add auto complete for searchEntry
        self.search_input_label = QLabel("Search Text:", self.searchEntryWidget)
        self.search_input = QLineEdit(self.searchEntryWidget)
        self.search_input.setCompleter(self.completer2)
        self.clear_button = QtWidgets.QPushButton("Clear", self.searchEntryWidget)
        self.clear_button.clicked.connect(self.clearButton)


        #Where the contents of the "Search Entry" or "Search Positive Cases" are displayed
        self.file_content_text_edit = QTextEdit(self.searchEntryWidget)
        self.file_content_text_edit.setReadOnly(True)
        #Layout of Search Entry
        search_entry_layout.addWidget(self.search_input_label)
        search_entry_layout.addWidget(self.search_input)
        search_entry_layout.addWidget(self.file_content_text_edit)
        search_entry_layout.addWidget(self.positive_count_label) 
        search_entry_layout.addWidget(self.search_positive_button) 
        search_entry_layout.addWidget(self.clear_button)
        # Add both views to the stacked widget
        self.stacked_widget.addWidget(self.addEntryWidget)
        self.stacked_widget.addWidget(self.searchEntryWidget)

        # Create the Add Entry,Search Entry, & Toggle theme buttons
        self.addEntryButton = QtWidgets.QPushButton("Add Entry")
        self.addEntryButton.clicked.connect(self.show_add_entry_view)

        self.searchEntryButton = QtWidgets.QPushButton("Search Entry")
        self.searchEntryButton.clicked.connect(self.show_search_entry_view)

        self.toggle_button = QPushButton("Toggle Theme", self.addEntryWidget)
        self.toggle_button.clicked.connect(self.toggle_theme)


        #Layout of the program
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.addEntryButton)
        layout.addWidget(self.searchEntryButton)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.stacked_widget)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 400, 600)

        self.completer2.activated.connect(self.display_file_content)

        #Light mode stylesheet
        self.light_mode_stylesheet = ("""
            QLabel {
                font-size: 20px;
                color: #333333;
            }
            QTextEdit {
                font-size: 20px;
                color: black; 
                background-color: #dddddd; 
                border: 1px solid #999999; 
                border-radius: 5px;
                padding: 5px;
            }
            QRadioButton {
                font-size: 20px;
                color: #333333;
            }
            QLineEdit {
                font-size: 20px;
                color: black; 
                background-color: #dddddd; 
                border: 1px solid #999999; 
                border-radius: 5px;
                padding: 5px;
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

        #Dark Mode stylesheet
        self.dark_mode_stylesheet = ("""
            
            QWidget {
                background-color: black;
            }
            QTextEdit {
                font-size: 20px;
                color: white; 
                background-color: #222222; 
                border: 1px solid #666666; 
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 20px;
                color: white; 
                background-color: #222222; 
                border: 1px solid #666666; 
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                font-size: 20px;
                color: #cccccc;
            }
            QRadioButton {
                font-size: 20px;
                color: #cccccc;
            }
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #474747;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #363461;
            }
        """)

        self.light_mode = True
        self.setStyleSheet(self.light_mode_stylesheet)
        self.update_toggle_button_text()

    def main(self):
        self.window.show()
        self.app.exec_()

    def show_add_entry_view(self):
        self.stacked_widget.setCurrentWidget(self.addEntryWidget)

    def show_search_entry_view(self):
        self.stacked_widget.setCurrentWidget(self.searchEntryWidget)

    #Clears the texts in all of the Search Entry's Fields
    def clearButton(self):
        self.search_input.clear()
        self.file_content_text_edit.clear()

    #Searches for the date & places of positive cases & counts them
    def search_positive_cases(self):
        folder_path = "C:/Users/ASUS/Desktop/Visual Studio Code Projects/FINAL PROJECT OOP/Contract-Tracing-App/TextFiles"
        positive_count = 0
        positive_cases_info = []

        if os.path.exists(folder_path):
            try:
                file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                for file_name in file_names:
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, "r") as file:
                        file_content = file.read()
                        if "Covid-19 Test Status: Yes - Positive" in file_content:
                            positive_count += 1

                            # Use regular expressions to find date and place information
                            date_match = re.search(r"Date: (\d{4}-\d{2}-\d{2})", file_content)
                            place_match = re.search(r"Last Place Visited: (.+)", file_content)

                            if date_match and place_match:
                                date_str = date_match.group(1)
                                place_info = place_match.group(1)
                                positive_cases_info.append(f"Date: {date_str}, Place: {place_info}, \nCovid Test Status: Yes - Positive \n")

                self.positive_count_label.setText(f"Positive Cases Count: {positive_count}")
                self.file_content_text_edit.setPlainText("Places & Dates Of Confirmed Cases: \n \n" + "\n".join(positive_cases_info))

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while searching for positive cases: {e}")

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

    # Displays the contents of the searched text files
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

        #Sets covid option label based on the radio buttons
        covid_option = ""
        if self.covid_no_button.isChecked():
            covid_option = "Not Yet Tested"
        elif self.covid_pending_button.isChecked():
            covid_option = "Yes - Pending"
        elif self.covid_negative_button.isChecked():
            covid_option = "Yes - Negative"
        elif self.covid_positive_button.isChecked():
            covid_option = "Yes - Positive"

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
                file.write("Covid-19 Test Status: " + covid_option + "\n")
                file.write("Date: " +  now.toString(Qt.ISODate) + "\n")
            QMessageBox.information(self, "Success", "Data saved successfully!")

            #Clears add entry widget for new input
            self.clear_text_fields()
            self.clear_radio_buttons()

            #Utilizes the autocompleter to search and load entries from the folder
            searchEntry = self.load_entries_from_folder()
            self.completer2.setModel(QtCore.QStringListModel(searchEntry))
            self.search_input.setCompleter(self.completer2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the text: {e}")

    #Clears text fields in the Add Entry Widget
    def clear_text_fields(self):
        self.name_input.clear()
        self.age_input.clear()
        self.address_input.clear()
        self.contact_input.clear()
        self.places_input.clear()

    #Clears the radio buttons in the Add Entry Widget
    def clear_radio_buttons(self):
        self.dummy_radio_button.setChecked(True)

    #Is connected to the toggle theme button, which allows the user to switch from dark mode to light mode
    def toggle_theme(self):
        if self.light_mode:
            self.setStyleSheet(self.dark_mode_stylesheet)
        else:
            self.setStyleSheet(self.light_mode_stylesheet)

        self.light_mode = not self.light_mode
        self.update_toggle_button_text()

    #Updates the button label everytime the user clicks the toggle button
    def update_toggle_button_text(self):
        if self.light_mode:
            self.toggle_button.setText("Toggle Dark Mode")
        else:
            self.toggle_button.setText("Toggle Light Mode")

#Runs the main program
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = GUI()
    window.show()
    app.exec_()
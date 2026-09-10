import sys
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QLabel,
    QFrame,
    QDialog,
)


# ============================================================
# FILE SETTINGS
# ============================================================

DATA_FILE = "database.json"


# ============================================================
# CUSTOM DELETE CONFIRMATION
# ============================================================

class DeleteDialog(QDialog):

    def __init__(self, name, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Confirm Delete")
        self.setFixedSize(420, 210)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        self.setLayout(layout)

        # Title
        title = QLabel("Confirm Delete")
        title.setObjectName("dialogTitle")

        layout.addWidget(title)

        # Message
        message = QLabel(
            f"Are you sure you want to delete\n"
            f"'{name}' from the database?"
        )

        message.setObjectName("dialogMessage")
        message.setAlignment(Qt.AlignCenter)

        layout.addWidget(message)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        cancel_button = QPushButton("Cancel")
        delete_button = QPushButton("Delete")

        cancel_button.setObjectName("cancelButton")
        delete_button.setObjectName("deleteButton")

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        cancel_button.clicked.connect(self.reject)
        delete_button.clicked.connect(self.accept)

        # Dialog style
        self.setStyleSheet("""

            QDialog {
                background-color: #1E1E1E;
            }

            QLabel#dialogTitle {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: bold;
            }

            QLabel#dialogMessage {
                color: #CCCCCC;
                font-size: 14px;
            }

            QPushButton {
                min-height: 40px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#cancelButton {
                background-color: #3A3A3A;
                color: white;
                border: none;
            }

            QPushButton#cancelButton:hover {
                background-color: #4A4A4A;
            }

            QPushButton#deleteButton {
                background-color: #D64545;
                color: white;
                border: none;
            }

            QPushButton#deleteButton:hover {
                background-color: #E45B5B;
            }

        """)


# ============================================================
# MAIN WINDOW
# ============================================================

class PersonalDatabase(QMainWindow):

    def __init__(self):
        super().__init__()

        self.database = {}

        self.setWindowTitle(
            "Personal Data Management System"
        )

        self.setMinimumSize(850, 600)
        self.resize(1000, 700)

        self.load_data()
        self.setup_ui()
        self.refresh_table()

    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(self):

        if os.path.exists(DATA_FILE):

            try:

                with open(
                    DATA_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.database = json.load(file)

            except (json.JSONDecodeError, OSError):

                self.database = {}

    # ========================================================
    # SAVE DATA
    # ========================================================

    def save_data(self):

        try:

            with open(
                DATA_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.database,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Save Error",
                f"Could not save data.\n\n{error}"
            )

    # ========================================================
    # USER INTERFACE
    # ========================================================

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            25, 25, 25, 25
        )

        main_layout.setSpacing(18)

        central_widget.setLayout(main_layout)

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel(
            "Personal Data Management System"
        )

        title.setObjectName("title")

        subtitle = QLabel(
            "Add, search, update and manage your personal data"
        )

        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ----------------------------------------------------
        # INPUT CARD
        # ----------------------------------------------------

        input_card = QFrame()
        input_card.setObjectName("card")

        input_layout = QVBoxLayout()

        input_layout.setContentsMargins(
            20, 20, 20, 20
        )

        input_layout.setSpacing(15)

        input_card.setLayout(input_layout)

        # ----------------------------------------------------
        # FORM
        # ----------------------------------------------------

        form_layout = QFormLayout()

        form_layout.setSpacing(12)

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Enter name"
        )

        self.meaning_input = QLineEdit()

        self.meaning_input.setPlaceholderText(
            "Enter name meaning"
        )

        form_layout.addRow(
            "Name:",
            self.name_input
        )

        form_layout.addRow(
            "Meaning:",
            self.meaning_input
        )

        input_layout.addLayout(form_layout)

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.setSpacing(10)

        self.add_button = QPushButton("Add")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.clear_button = QPushButton("Clear")

        self.add_button.setObjectName(
            "addButton"
        )

        self.update_button.setObjectName(
            "updateButton"
        )

        self.delete_button.setObjectName(
            "deleteButton"
        )

        self.clear_button.setObjectName(
            "clearButton"
        )

        button_layout.addWidget(
            self.add_button
        )

        button_layout.addWidget(
            self.update_button
        )

        button_layout.addWidget(
            self.delete_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        input_layout.addLayout(
            button_layout
        )

        main_layout.addWidget(
            input_card
        )

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        search_layout = QHBoxLayout()

        search_label = QLabel("Search:")
        search_label.setObjectName(
            "searchLabel"
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search by name or meaning..."
        )

        search_layout.addWidget(
            search_label
        )

        search_layout.addWidget(
            self.search_input
        )

        main_layout.addLayout(
            search_layout
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            [
                "Name",
                "Meaning"
            ]
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        self.table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(
            False
        )

        main_layout.addWidget(
            self.table
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = QLabel()

        self.status_label.setObjectName(
            "statusLabel"
        )

        main_layout.addWidget(
            self.status_label
        )

        # ----------------------------------------------------
        # SIGNALS
        # ----------------------------------------------------

        self.add_button.clicked.connect(
            self.add_data
        )

        self.update_button.clicked.connect(
            self.update_data
        )

        self.delete_button.clicked.connect(
            self.delete_data
        )

        self.clear_button.clicked.connect(
            self.clear_inputs
        )

        self.search_input.textChanged.connect(
            self.search_data
        )

        self.table.itemSelectionChanged.connect(
            self.select_table_row
        )

        self.name_input.returnPressed.connect(
            self.go_to_meaning
        )

        self.meaning_input.returnPressed.connect(
            self.add_data
        )
        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        self.setStyleSheet("""

            QMainWindow {
                background-color: #121212;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 14px;
                color: #F5F5F5;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #FFFFFF;
            }

            QLabel#subtitle {
                font-size: 14px;
                color: #9E9E9E;
            }

            QFrame#card {
                background-color: #1E1E1E;
                border: 1px solid #303030;
                border-radius: 14px;
            }

            QLineEdit {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 11px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #00C2FF;
            }

            QLabel#searchLabel {
                font-weight: bold;
                font-size: 15px;
            }

            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 11px 18px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#addButton {
                background-color: #00C2FF;
                color: #081014;
            }

            QPushButton#addButton:hover {
                background-color: #33CEFF;
            }

            QPushButton#updateButton {
                background-color: #7C4DFF;
                color: white;
            }

            QPushButton#updateButton:hover {
                background-color: #9068FF;
            }

            QPushButton#deleteButton {
                background-color: #D64545;
                color: white;
            }

            QPushButton#deleteButton:hover {
                background-color: #E45B5B;
            }

            QPushButton#clearButton {
                background-color: #3A3A3A;
                color: white;
            }

            QPushButton#clearButton:hover {
                background-color: #4A4A4A;
            }

            QTableWidget {
                background-color: #1E1E1E;
                alternate-background-color: #242424;
                border: 1px solid #303030;
                border-radius: 10px;
                gridline-color: #353535;
                selection-background-color: #24566A;
                selection-color: white;
            }

            QTableWidget::item {
                padding: 10px;
            }

            QHeaderView::section {
                background-color: #2D2D2D;
                color: #FFFFFF;
                padding: 11px;
                border: none;
                border-bottom: 1px solid #444444;
                font-weight: bold;
            }

            QLabel#statusLabel {
                color: #8F8F8F;
                font-size: 13px;
            }

        """)

    # ========================================================
    # ADD DATA
    # ========================================================

    def add_data(self):

        name = self.name_input.text().strip()
        meaning = self.meaning_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Missing Name",
                "Please enter a name."
            )

            self.name_input.setFocus()

            return

        if not meaning:

            QMessageBox.warning(
                self,
                "Missing Meaning",
                "Please enter the meaning."
            )

            self.meaning_input.setFocus()

            return

        if name in self.database:

            QMessageBox.warning(
                self,
                "Already Exists",
                f"'{name}' already exists.\n\n"
                "Use Update to change its meaning."
            )

            return

        self.database[name] = meaning

        self.save_data()

        self.refresh_table()

        self.clear_inputs()

        self.status_label.setText(
            f"'{name}' added successfully."
        )

    # ========================================================
    # UPDATE DATA
    # ========================================================

    def update_data(self):

        # Get selected row
        selected_rows = self.table.selectionModel().selectedRows()

        # No row selected
        if not selected_rows:
            QMessageBox.warning(
                self,
                "No Record Selected",
                "Please select a record from the table first."
            )
            return

        # Get selected row number
        row = selected_rows[0].row()

        # Get name from selected row
        name_item = self.table.item(row, 0)

        if name_item is None:
            QMessageBox.warning(
                self,
                "Error",
                "Could not read the selected record."
            )
            return

        name = name_item.text().strip()

        # Get new meaning from input box
        new_meaning = self.meaning_input.text().strip()

        if not new_meaning:
            QMessageBox.warning(
                self,
                "Missing Meaning",
                "Please enter the new meaning."
            )
            self.meaning_input.setFocus()
            return

        # Check that record still exists
        if name not in self.database:
            QMessageBox.warning(
                self,
                "Record Not Found",
                f"'{name}' was not found in the database."
            )
            return

        # Update the database
        self.database[name] = new_meaning

        # Save data
        self.save_data()

        # Update the selected table row directly
        self.table.setItem(
            row,
            1,
            QTableWidgetItem(new_meaning)
        )

        # Keep the selected row
        self.table.selectRow(row)

        # Update status
        self.status_label.setText(
            f"'{name}' updated successfully."
        )

    # ========================================================
    # DELETE DATA
    # ========================================================

    def delete_data(self):

        # First check the selected table row
        selected_rows = self.table.selectionModel().selectedRows()

        # If a row is selected, get its name
        if selected_rows:

            row = selected_rows[0].row()

            name_item = self.table.item(row, 0)

            if name_item:
                name = name_item.text().strip()
            else:
                name = ""

        else:

            # Otherwise use name input
            name = self.name_input.text().strip()

        # Check name
        if not name:

            QMessageBox.warning(
                self,
                "No Data Selected",
                "Please select a record from the table "
                "or enter a name."
            )

            return

        # Check if it exists
        if name not in self.database:

            QMessageBox.warning(
                self,
                "Not Found",
                f"'{name}' does not exist in the database."
            )

            return

        # ----------------------------------------------------
        # CUSTOM CONFIRMATION DIALOG
        # ----------------------------------------------------

        dialog = DeleteDialog(
            name,
            self
        )

        result = dialog.exec_()

        # User clicked Delete
        if result == QDialog.Accepted:

            del self.database[name]

            self.save_data()

            self.refresh_table()

            self.clear_inputs()

            self.status_label.setText(
                f"'{name}' deleted successfully."
            )

    # ========================================================
    # SEARCH
    # ========================================================

    def search_data(self, text):

        search_text = text.strip().lower()

        for row in range(
            self.table.rowCount()
        ):

            name_item = self.table.item(
                row,
                0
            )

            meaning_item = self.table.item(
                row,
                1
            )

            if not name_item:
                continue

            name = name_item.text().lower()

            meaning = meaning_item.text().lower()

            match = (
                search_text in name
                or search_text in meaning
            )

            self.table.setRowHidden(
                row,
                not match
            )

    # ========================================================
    # REFRESH TABLE
    # ========================================================

    def refresh_table(self):

        self.table.setRowCount(0)

        for name, meaning in self.database.items():

            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(name)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(meaning)
            )

        self.status_label.setText(
            f"Total records: {len(self.database)}"
        )

    # ========================================================
    # SELECT TABLE ROW
    # ========================================================

    def select_table_row(self):

        selected_rows = (
            self.table
            .selectionModel()
            .selectedRows()
        )

        if not selected_rows:
            return

        row = selected_rows[0].row()

        name_item = self.table.item(
            row,
            0
        )

        meaning_item = self.table.item(
            row,
            1
        )

        if name_item and meaning_item:

            self.name_input.setText(
                name_item.text()
            )

            self.meaning_input.setText(
                meaning_item.text()
            )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_inputs(self):

        self.name_input.clear()
        self.meaning_input.clear()

        self.status_label.setText(
            f"Total records: {len(self.database)}"
        )

        self.name_input.setFocus()
#____________________________________________________________
    def go_to_meaning(self):
        """Move to the meaning field when Enter is pressed."""

        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Missing Name",
                "Please enter a name first."
            )
            self.name_input.setFocus()
            return

            if name in self.database:
                QMessageBox.warning(
                    self,
                    "Already Exists",
                    f"'{name}' already exists in the database.\n\n"
                    "Use Update to change its meaning."
                )

            self.name_input.selectAll()
            self.name_input.setFocus()
            return

        self.meaning_input.setFocus()

# ============================================================
# START APPLICATION
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Personal Data Management System"
    )

    app.setFont(
        QFont("Segoe UI", 10)
    )

    window = PersonalDatabase()

    window.show()

    sys.exit(
        app.exec_()
    )

#___________________________________________________________________________


#___________________________________________________________________________
if __name__ == "__main__":
    main()
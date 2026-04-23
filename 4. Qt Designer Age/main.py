import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

app = QApplication(sys.argv)

loader = QUiLoader()
ui_file = QFile("MainWindow.ui")
ui_file.open(QFile.ReadOnly)
window = loader.load(ui_file)
ui_file.close()

# اتصال دکمه
def calculate_age():
    try:
        age_text = window.Input_Age.toPlainText()
        age = int(age_text)

        if age < 18:
            window.Label.setText("You are under 18")
        elif age < 65:
            window.Label.setText("You are an adult")
        else:
            window.Label.setText("You are a senior")

    except ValueError:
        window.Label.setText("Please enter a valid number")

window.pushButton.clicked.connect(calculate_age)

window.show()
sys.exit(app.exec())
from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('test1.ui', self)

        central = self.findChild(QtWidgets.QWidget, 'centralwidget')

        self.enterButton = self.findChild(QtWidgets.QPushButton, 'button')
        self.enterButton.clicked.connect(self.send_message)

        self.input = self.findChild(QtWidgets.QLineEdit, "input")
        
        self.output = self.findChild(QtWidgets.QTextBrowser, "output")
        self.output.append("test")

    def send_message(self):
        self.output.append(self.input.text())
        self.input.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
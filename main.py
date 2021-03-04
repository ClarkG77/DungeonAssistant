from PyQt5 import QtWidgets, uic
import parseResponse
from watsonAssistant import Assistant
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.assistant = Assistant()
        self.mainApp = app

        #Load the UI Page
        uic.loadUi('main.ui', self)

        self.enterButton = self.findChild(QtWidgets.QPushButton, 'button')
        self.enterButton.clicked.connect(self.send_message)

        self.input = self.findChild(QtWidgets.QLineEdit, "input")
        self.input.returnPressed.connect(self.send_message)
        
        self.outputScroll = self.findChild(QtWidgets.QScrollArea, "scrollArea")
        self.outputWidget = self.findChild(QtWidgets.QWidget, "scrollAreaWidgetContents")
        self.outputLayout = self.findChild(QtWidgets.QVBoxLayout, "layoutArea")

        self.outputWidget.setLayout(self.outputLayout)
        self.outputScroll.setWidget(self.outputWidget)

        

    def send_message(self):
        new_input = self.input.text()
        self.print(new_input)
        self.input.clear()

        response = self.assistant.getResponse(new_input)
        print(str(response))
        #parse response here then append it
        response = parseResponse.parseResponse(response)
        self.print(response)
        
    def print_response(self,response):
        for label in res:
            #just print text
            if label['response_type']=='text':
                print_text(label['text'])
            #description -> source
            elif label['response_type']=='image':
                print_text(label['description'])
                print_image(label['source'])
            #title -> description -> buttons ie options
            elif label['response_type']=='option':
                print_text(label['title'])
                print_text(label['description'])
                print_button(['options'])
    def print_text(self, message):
        newLabel = QtWidgets.QLabel(self.outputWidget)
        newLabel.setText(message)
        newLabel.setWordWrap(True)
        newLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        newLabel.setOpenExternalLinks(True)

        self.outputLayout.addWidget(newLabel)
        newLabel.show()

        self.mainApp.processEvents()
        self.outputScroll.ensureWidgetVisible(newLabel)
    def print_image(self,source):
        
        pass
    def print_button(self,options):
        
        pass
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
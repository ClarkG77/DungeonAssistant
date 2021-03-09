from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QImage, QPixmap
import requests
import parseResponse
from watsonAssistant import Assistant
from buttonBar import ButtonBar
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
        self.print_text(new_input, alignRight=True)
        self.input.clear()
        response = self.assistant.getResponse(new_input)
        print(str(response))        
        #parse response here then append it
        self.print_response(response)
        #response = parseResponse.parseResponse(response)
        #self.print_response(response)
        

    def print_response(self,response):
        for label in response:
            #just print text
            if label['response_type']=='text':
                self.print_text(label['text'])
            #description -> source
            elif label['response_type']=='image':
                #check if image or gif
                if False:
                    pass
                else:
                    self.print_image(label['source'])
                self.print_text(label['description'])
                
                
            #title -> description -> buttons ie options
            elif label['response_type']=='option':
                if 'title' in label:
                    self.print_text(label['title'])
                if 'description' in label:
                    self.print_text(label['description'])
                self.print_option(label)

    #the last lines of each of these should be converted to a new function to generally display things

    def print_buttons(self, labels, values):
        buttonBar = ButtonBar(self, labels, values, self.outputWidget)
        self.outputLayout.addWidget(buttonBar.groupBox)
        buttonBar.show()

        self.mainApp.processEvents()
        self.outputScroll.ensureWidgetVisible(buttonBar.groupBox)


    def print_text(self, message, alignRight=False):
        newLabel = QtWidgets.QLabel(self.outputWidget)
        newLabel.setText(message)
        newLabel.setWordWrap(True)
        newLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        newLabel.setOpenExternalLinks(True)

        if(alignRight):
            newLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.outputLayout.addWidget(newLabel)
        newLabel.show()

        self.mainApp.processEvents()
        self.outputScroll.ensureWidgetVisible(newLabel)

    #QMovie is what will play gifs we will likely need a way to auto pause these as they will probably continue playing
    def print_image(self,source):
        image = QImage()
        image.loadFromData(requests.get(source).content)
        image_label = QtWidgets.QLabel()
        image_label.setPixmap(QPixmap(image))
        self.outputLayout.addWidget(image_label)
        image_label.show()
    #currently defined for monster search only
    def print_option(self,label):
        text=[]
        values=[]
        for option in label['options']:
            text.append(option['label'])
            values.append(option['value']['input']['text'])
        print(text)
        print(values)
        self.print_buttons(text,values)
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
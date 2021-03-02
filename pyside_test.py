from PyQt5 import QtWidgets, uic
import parseResponse
from watsonAssistant import Assistant
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys

auth_key='5rk0dj6q2qhHmlpgWm1SNJFUS_0M6uBYaGxqpPhNUGDC'
serv_url='https://api.us-south.assistant.watson.cloud.ibm.com/instances/02ca2e28-abb4-40c4-bb83-55fd22306435'
asst_id='6f4e748c-9409-48d6-a202-b2b8dc738351'

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.assistant = Assistant()

        #Load the UI Page
        uic.loadUi('test1.ui', self)

        self.enterButton = self.findChild(QtWidgets.QPushButton, 'button')
        self.enterButton.clicked.connect(self.send_message)

        self.input = self.findChild(QtWidgets.QLineEdit, "input")
        self.input.returnPressed.connect(self.send_message)
        
        self.output = self.findChild(QtWidgets.QTextBrowser, "output")
        

    def send_message(self):
        new_input = self.input.text()
        self.output.append(new_input)

        #response = get_response_text(self.assistant, asst_id, self.sesh_id, new_input)
        response = self.assistant.getResponse(new_input)
        response = parseResponse.parseResponse(response)
        #parse response here then append it
        self.output.append(response)
        self.input.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
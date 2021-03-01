from PyQt5 import QtWidgets, uic
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys

auth_key='5rk0dj6q2qhHmlpgWm1SNJFUS_0M6uBYaGxqpPhNUGDC'
serv_url='https://api.us-south.assistant.watson.cloud.ibm.com/instances/02ca2e28-abb4-40c4-bb83-55fd22306435'
asst_id='6f4e748c-9409-48d6-a202-b2b8dc738351'

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
        new_input = self.input.text()
        self.output.append(new_input)

        response = get_response_text(self.assistant, asst_id, self.sesh_id, new_input)
        
        self.output.append(str(response))
        self.input.clear()

    def start_assistant(self):
       self.assistant = create_assistant()
       self.sesh_id = create_session(self.assistant)


def create_assistant():
    authenticator = IAMAuthenticator(auth_key)
    assistant = AssistantV2(
        version='2021-02-16',
        authenticator=authenticator
    )
    assistant.set_service_url(serv_url)

    return assistant

def create_session(assistant):
    sesh_id = assistant.create_session(
        assistant_id=asst_id
    ).get_result()['session_id']

    return sesh_id

def get_response_text(assistant, asst_id, sesh_id, message):
    response = assistant.message(
        assistant_id=asst_id,
        session_id=sesh_id,
        input={
            'message_type': 'text',
            'text': message,
        }
    ).get_result()

    return response['output']['generic']

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.start_assistant()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
import json
import tkinter as tk
from tkinter import scrolledtext
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

auth_key='5rk0dj6q2qhHmlpgWm1SNJFUS_0M6uBYaGxqpPhNUGDC'
serv_url='https://api.us-south.assistant.watson.cloud.ibm.com/instances/02ca2e28-abb4-40c4-bb83-55fd22306435'
asst_id='6f4e748c-9409-48d6-a202-b2b8dc738351'

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


assistant = create_assistant()
sesh_id = create_session(assistant)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        master.bind('<Return>', self.enter_button)

    def create_widgets(self):
        self.text = scrolledtext.ScrolledText(self)
        self.text.insert(tk.INSERT, "Hello World!")
        self.text.configure(state ='disabled') 
        self.text.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.enter = tk.Button(self, text="Enter", fg="black", command=self.enter_button)
        self.enter.pack(side="bottom")

        self.input = tk.Entry(self)
        self.input.pack(side="bottom")

        

    def enter_button(self, _event=None):
    	new_input = self.input.get()
    	output = "\n" + new_input

    	self.input.delete(0,'end')

    	response = get_response_text(assistant, asst_id, sesh_id, new_input)
    	output += "\n" + str(response)

    	self.text.configure(state ='normal') 
    	self.text.insert(tk.END, output)
    	self.text.see(tk.END)
    	self.text.configure(state ='disabled') 
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()

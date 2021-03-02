import json

#takes the json response and parses it out into a string for us to use
def parseResponse(res):
    response=''
    for label in res:
        if label['response_type']=='text':
            response+=label['text']
            print(label['text'])
    return response


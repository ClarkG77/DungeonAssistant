import json
linkTemplate = '<a target="_blank" href={0}>{1}</a>'
#takes the json response and parses it out into a string for us to use
#still missing options button stuff and will likely need to cha
def parseResponse(res):
    response=''
    for label in res:
        if label['response_type']=='text':
            response+=label['text']
            print(label['text'])
        elif label['response_type']=='image':
            response+='<a href='+label['source']+'></a>'+label['description']
        elif label['response_type']=='option':
            response+=label['title']
            #spaced for possible button creation between
            response+=label['description']
    return response


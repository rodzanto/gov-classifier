import json
import boto3
import os
from datetime import datetime

#now = datetime.now()
#current_time = now.strftime("%Y%m%d%H%M%S")

current_time = datetime.now().strftime("%Y%m%d%H%M%S")

def lambda_handler(event, context):
    doc = event['doc']
    text = event['text']
    blocks = event['blocks']

    dynamodb = boto3.client('dynamodb')

    #respid = []
    #resptext = []
    response = json.loads('{}')
    
    
    # Print detected text
    for item in blocks:
        if item["BlockType"] == "LINE":
            #respid.append(item["Id"])
            #resptext.append(item["Text"])
            response.update({item["Id"]: {"S": item["Text"]}})
    
    #{respid[0]: {"S": resptext[0]} }
    
    print(json.dumps(response))
    #print(respid)
    

    dynamodb.put_item(TableName='gov-metadata', Item={'times':{'N':current_time}, 'doc':{'S':doc['Name']},'full-doc':{'S':json.dumps(doc)},'linen':{"M": response}})
        
    return "Successfully stored the document metadata for " + doc['Name'] + " on timestamp " + current_time

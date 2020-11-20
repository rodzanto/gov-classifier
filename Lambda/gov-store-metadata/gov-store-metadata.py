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
    DDB_METADATA_TABLE = os.environ['DDB_METADATA_TABLE']
    DDB_CONFIG_TABLE = os.environ['DDB_CONFIG_TABLE']

    dynamodb = boto3.client('dynamodb')

    #respid = []
    #resptext = []
    response = json.loads('{}')
    
    filtered_response = {}
    
    #retrieve config for the document type
    
    config=dynamodb.get_item(TableName=DDB_CONFIG_TABLE, Key={'doc':{'S': doc['Name']}}, ProjectionExpression='relevantlines')
    
    
    if 'Item' in config: 
        lines = json.loads(config['Item']['relevantlines']['S'])
        
    index = 0
    # Print detected text
    for item in blocks:
        if item["BlockType"] == "LINE":            
            if 'Item' in config:                
                if  index in lines:
                    print('Inserto')
                    response.update({item["Id"]: {"S": item["Text"]}})
            else:
                response.update({item["Id"]: {"S": item["Text"]}})
            index+=1
    
    
    
    print(json.dumps(response))
    
            

    dynamodb.put_item(TableName=DDB_METADATA_TABLE, Item={'times':{'N':current_time}, 'doc':{'S':doc['Name']},'full-doc':{'S':json.dumps(doc)},'linen':{"M": response}})
        
    return "Successfully stored the document metadata for " + doc['Name'] + " on timestamp " + current_time

import boto3
import json
import os

CUSTOM_CLASSIFIER_ARN = os.environ['CUSTOM_CLASSIFIER_ARN']

def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    file_key = event['file_key']
    imageresult = event['imageresult']
    
    ###Textract
    
    client = boto3.client('textract')
    #process using S3 object
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket_name, 'Name': file_key}}
    )
    #Get the text blocks
    blocks=response['Blocks']

    # Print detected text
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text = text + " " +  item["Text"]
    
    print(text)

    ###Comprehend Custom  - Commenting out for now              
    
    #client = boto3.client('comprehend', region_name='eu-west-1')
    #response = client.classify_document(
    #    Text=json.dumps(text),
    #    EndpointArn=CUSTOM_CLASSIFIER_ARN
    #)

    #print(response)

    labels = response['Classes']

    ### Choose best classifier
    #TBD... choosing Rekognition Custom Labels for now

    if len(labels):
        print("Got {} labels".format(len(labels)))
        print(labels)
        
        metadata = {"doc":imageresult[0], "text": text, "blocks": "blocks"}
        
        return metadata
    else:
        return "Invalid or unknown document"

import boto3
import time
import json
import base64

def to_id(_num, _base=62):
    if _num <= 0: return '0'
    charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    res = ''
    while _num:
        rem = _num % _base
        _num //= _base
        res += charset[rem]
    return res

def upload_to_s3(event, context):
    # print(event)
    # print(event['body'])   
    print("entered")

    s3 = boto3.client('s3', 
                      aws_access_key_id="AKIAQB2AUH6FWWNFCK63", 
                      aws_secret_access_key="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", 
                      region_name="ap-south-1"
                      )
    bucket_name = 'handwriter'
    cur_time = to_id(time.time_ns())
    s3_sub_path = "submission_{}.jpg".format(cur_time)

    print('body is', event['body'])
    print('type of body is', event['body'])

    print('upl is', json.loads(event['body'])['upl_hw'])


    upl_hw = base64.b64decode(json.loads(event['body'])['upl_hw'])
    s3.put_object(
        Bucket=bucket_name,
        Key=s3_sub_path,
        Body=upl_hw,
        ContentType='image/jpeg',
        ACL='public-read'
    )
    return {
        'statusCode': 200,
        'body': {
        'path' : 'https://handwriter.s3.ap-south-1.amazonaws.com/{}'.format(s3_sub_path)
        }
    }

# AWS Lambda handler
def lambda_handler(event, context):
    return upload_to_s3(event, context)

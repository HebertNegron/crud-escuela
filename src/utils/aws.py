import boto3
from os import environ as env
from boto3.dynamodb.conditions import Attr

def create_client(type: str):
    return boto3.client(type,
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=env.get("AWS_SESSION_TOKEN"),
            region_name=env.get("REGION_NAME")
        )

def create_resource(type: str):
    return boto3.resource(type,
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=env.get("AWS_SESSION_TOKEN"),
            region_name=env.get("REGION_NAME")
        )
    
def upload_file_to_s3(file, filename) -> None:
    s3 = create_client('s3')
    s3.upload_file(
        file,
        env.get('BUCKET_NAME'),
        filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": 'multipart/form-data'
        }
    )

def publish_message_to_sns(message: str, topic_arn: str) -> None:
    sns = create_client('sns')
    sns.publish(
        TopicArn=topic_arn,
        Message=message
    )

def put_item_to_dynamodb(table_name: str, item: dict) -> None:
    dynamodb = create_resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(
        Item=item
    )

def scan_table(table_name: str, filter_expression: Attr) -> list[dict]:
    dynamodb = create_resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression=filter_expression
    )
    return response['Items']

def update_item_in_dynamodb(table_name: str, key: dict, update_expression: str, expression_attribute_values: dict) -> None:
    dynamodb = create_resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
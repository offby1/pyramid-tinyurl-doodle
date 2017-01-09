import logging

import botocore
import boto3
from boto3.dynamodb.conditions import Attr

_log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

ddb = boto3.resource('dynamodb')
table = ddb.Table('hashes-test')


for item in table.scan()['Items']:
    try:
        table.update_item(Key={'human_hash': item['human_hash']},
                          UpdateExpression='set create_day = :create_day',
                          ConditionExpression=Attr('create_day').not_exists(),
                          ExpressionAttributeValues= {
                              ':create_day': item['create_date'][0:10],
                          })

    except botocore.exceptions.ClientError as e:
        if e.response.get('Error').get('Code') == 'ConditionalCheckFailedException':
            _log.info("Skipped {}".format(item['long_url']))
        else:
            raise
    else:
        _log.info("Updated {}".format(item['long_url']))

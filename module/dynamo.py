# Core
import datetime

# Third party
import boto3
import pytz

# Local
import database


def utcnow_string():
    return str(datetime.datetime.now (pytz.utc))


class DynamoDB(database.DatabaseMeta):

    # TODO -- allow region & credentials to be paramaterizable?
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')
        self.table = self.ddb.Table('hashes')

    def save(self, key, value):
        self.table.put_item(Item={'human_hash': key,
                                  'long_url': value,
                                  'create_date': utcnow_string()})

    def lookup(self, key):
        return self.table.get_item(Key={'human_hash': key})['Item']['long_url']

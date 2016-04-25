# Core
import datetime
import logging
import operator

# Third party
import botocore.exceptions
import boto3
import pytz

# Local
from . import database

_log = logging.getLogger(__name__)

class DynamoDB(database.DatabaseMeta):

    # TODO -- allow region & credentials to be paramaterizable?
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')
        self.table = self.ddb.Table('hashes')
        _log.info("Hello world")

    def save_or_update(self, key, value, create_date=None):
        if create_date is None:
            create_date = datetime.datetime.now (pytz.utc)

        try:
            self.table.put_item(Item={'human_hash': key,
                                      'long_url': value,
                                      'create_date': str(create_date)},
                            ConditionExpression='attribute_not_exists(human_hash)')
        # TODO -- this doesn't seem like a clean way to ignore "item already exists"
        except botocore.exceptions.ClientError:
            pass

    def lookup(self, key):
        response = self.table.get_item(Key={'human_hash': key})
        _log.debug("%s => %s", key, response)
        return response['Item']

    def get_all(self):
        # Yup, it's a scan.  They tell me that DynamoDB scans are
        # expensive.  But it's not obvious how else to do this ... and
        # anyway, nobody actually uses this web site.
        return sorted(self.table.scan()['Items'],
                      key=operator.itemgetter('create_date'),
                      reverse=True)

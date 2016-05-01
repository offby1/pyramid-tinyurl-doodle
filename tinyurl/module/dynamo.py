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

    def _validate_item(self, i):
        for k in 'human_hash', 'long_url', 'create_date':
            assert(k in i)

    def batch_add_key_value_pairs(self, items):
        create_date = datetime.datetime.now (pytz.utc).isoformat()
        with self.table.batch_writer() as batch:
            for i in items:
                i.setdefault('create_date', create_date)
                self._validate_item(i)
                batch.put_item(Item=i)
                _log.info("put %s", i['create_date'])

    def add_if_not_present(self, key, value):
        create_date = datetime.datetime.now (pytz.utc).isoformat()

        try:
            item = {'human_hash': key,
                    'long_url': value,
                    'create_date': create_date}
            self._validate_item(item)
            self.table.put_item(Item=item,
                                ConditionExpression='attribute_not_exists(human_hash)')

        except botocore.exceptions.ClientError as e:
            if e.response.get('Error').get('Code') != 'ConditionalCheckFailedException':
                raise

    def lookup(self, key):
        response = self.table.get_item(Key={'human_hash': key})
        _log.debug("%s => %s", key, response)
        return response['Item']

    def get_all(self):
        # Yup, it's a scan.  They tell me that DynamoDB scans are
        # expensive.  But it's not obvious how else to do this ... and
        # anyway, this web site gets so little use (12 inserts per
        # day, last I checked) that there's probably not that much
        # data to scan.
        return sorted(self.table.scan()['Items'],
                      key=operator.itemgetter('create_date'),
                      reverse=True)

    def delete(self, key):
        self.table.delete_item(Key={'human_hash': key})
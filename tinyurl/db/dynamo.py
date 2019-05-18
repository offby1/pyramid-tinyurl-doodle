# Core
import datetime
import logging
import operator

# Third party
import botocore.exceptions
import boto3
from boto3.dynamodb.conditions import Key
import pytz

_log = logging.getLogger(__name__)


def _iso_now():
    return datetime.datetime.now(pytz.utc).isoformat()


def _truncate_to_day(iso8601_string):
    return iso8601_string[0:10]


class DynamoDB:

    # TODO -- allow region & credentials to be paramaterizable?
    def __init__(self, table_name, daily_index_name):
        self.ddb = boto3.resource('dynamodb')
        self.daily_index_name = daily_index_name
        self.table = self.ddb.Table(table_name)

    def add_if_not_present(self, key, value):
        create_date = _iso_now()

        # Redundant, but handy as the hash key for a global secondary index
        create_day = _truncate_to_day(create_date)

        try:
            item = {
                'human_hash': key,
                'long_url': value,
                'create_date': create_date,
                'create_day': create_day,
            }

            self.table.put_item(
                Item=item, ConditionExpression='attribute_not_exists(human_hash)'
            )

        except botocore.exceptions.ClientError as e:
            if e.response.get('Error').get('Code') != 'ConditionalCheckFailedException':
                raise

    def lookup(self, key):
        response = self.table.get_item(Key={'human_hash': key})
        _log.debug("%s => %s", key, response)
        return response['Item']

    def get_all(self):
        # Yup, it's a scan.  They tell me that DynamoDB scans are
        # "expensive" (i.e., slow).  But it's not obvious how else to
        # do this ... and anyway, this web site gets so little use (12
        # inserts per day, last I checked) that there's probably not
        # that much data to scan.

        return sorted(
            self.table.scan()['Items'],
            key=operator.itemgetter('create_date'),
            reverse=True,
        )

    def get_one_days_hashes(self, date, later_than=None):
        date_string = date.isoformat()

        KeyConditionExpression = Key('create_day').eq(date_string)

        if later_than:
            KeyConditionExpression &= Key('create_date').gt(later_than.isoformat())

        QueryArgs = dict(
            IndexName=self.daily_index_name,
            Limit=10,
            KeyConditionExpression=KeyConditionExpression,
            ScanIndexForward=False,
        )
        result = self.table.query(**QueryArgs)
        return result['Items']

    def delete(self, key):
        self.table.delete_item(Key={'human_hash': key})

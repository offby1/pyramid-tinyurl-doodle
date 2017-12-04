# Core
import datetime
import logging
import operator

# Third party
import boto3
from boto3.dynamodb.conditions import Key

ddb = boto3.resource('dynamodb')
table = ddb.Table('hashes')


def lengthen_short_string(short_string):
    gotten = table.get_item(Key={'human_hash': short_string})
    return gotten.get('Item', {}).get('long_url')


def _fetch_one_day(day, max=10):
    date_string = day.isoformat()

    QueryArgs = dict(IndexName='create_day-create_date-index',
                     Limit=max,
                     KeyConditionExpression=Key('create_day').eq(date_string),
                     ScanIndexForward=False)
    result = table.query(**QueryArgs)
    return result['Items']



def a_few_recent_entries():
    """Returns the most recent entries in the hashes table, newest first.

    Makes multiple calls to _fetch_one_day, if needed; each call is
    expected to retrieve one day's worth of entries, ordered by
    creation time (newest first).

    :param day_fetcher: function of a date object that returns a list of dicts

    :yields: dicts from day_fetcher

    """

    items_to_fetch = 10

    most_recent_day = datetime.datetime.utcnow().date()

    for day_offset in range (0, -10, -1):
        day = most_recent_day + datetime.timedelta(days=day_offset)

        one_days_worth = _fetch_one_day(day, max=items_to_fetch)
        one_days_worth = sorted(one_days_worth,
                                key=operator.itemgetter('create_date'),
                                reverse=True)

        for item in one_days_worth:
            yield item
            items_to_fetch -= 1
            if items_to_fetch == 0:
                return

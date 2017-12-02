# Core
import logging
import operator

# Third party
import boto3

ddb = boto3.resource('dynamodb')
table = ddb.Table('hashes')

_log = logging.getLogger(__name__)


def get_some_entries_as_json ():
    # Yup, it's a scan.  They tell me that DynamoDB scans are
    # "expensive" (i.e., slow).  But it's not obvious how else to
    # do this ... and anyway, this web site gets so little use (12
    # inserts per day, last I checked) that there's probably not
    # that much data to scan.

    return sorted(table.scan(Limit=10)['Items'],
                  key=operator.itemgetter('create_date'),
                  reverse=True)

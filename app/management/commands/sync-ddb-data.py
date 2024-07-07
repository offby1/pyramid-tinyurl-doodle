import pathlib

import boto3
import tqdm
from app.models import ShortenedURL
from django.core.management.base import BaseCommand

__here__ = pathlib.Path(__file__).parent.resolve()


class Command(BaseCommand):
    def process_page(self, one_page_of_data):
        for item in one_page_of_data["Items"]:
            long_url = item["long_url"]["S"]
            create_date = item["create_date"]["S"]
            human_hash = item["human_hash"]["S"]
            existing = ShortenedURL.objects.filter(short=human_hash)
            if not existing.exists():
                ShortenedURL.objects.create(
                    created_at=create_date,
                    original=long_url,
                    short=human_hash,
                )

    # TODO -- push to dynamodb, in addition to pulling from it
    def handle(self, *args, **options):
        self.stdout.write("Hello? *thump* *thump* Is this thing on?")
        ddb_client = boto3.client(service_name="dynamodb")

        table_description = ddb_client.describe_table(TableName="hashes")

        LastEvaluatedKey = None
        progress_bar = tqdm.tqdm(total=table_description["Table"]["ItemCount"])
        while True:
            scan_args = dict(TableName="hashes")

            if LastEvaluatedKey is not None:
                scan_args["ExclusiveStartKey"] = LastEvaluatedKey

            one_page_of_data = ddb_client.scan(**scan_args)

            self.process_page(one_page_of_data)
            progress_bar.update(one_page_of_data["Count"])

            LastEvaluatedKey = one_page_of_data.get("LastEvaluatedKey")
            if LastEvaluatedKey is None:
                break

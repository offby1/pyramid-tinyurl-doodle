import pathlib

import boto3
import tqdm
from app.models import ShortenedURL
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand

__here__ = pathlib.Path(__file__).parent.resolve()


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_count = 0
        self.already_existed_count = 0
        self.hashes_in_dynamo = set()

    def _ingest_one_page_from_dynamo(self, one_page_of_data):
        for item in one_page_of_data["Items"]:
            long_url = item["long_url"]["S"]
            create_date = item["create_date"]["S"]
            human_hash = item["human_hash"]["S"]
            self.hashes_in_dynamo.add(human_hash)

            _, created = ShortenedURL.objects.get_or_create(
                short=human_hash,
                defaults=dict(
                    created_at=create_date,
                    original=long_url,
                ),
            )
            if created:
                self.created_count += 1
            else:
                self.already_existed_count += 1

    def download(self, *, ddb_client, TableName):
        table_description = ddb_client.describe_table(TableName=TableName)
        LastEvaluatedKey = None
        progress_bar = tqdm.tqdm(
            total=table_description["Table"]["ItemCount"],
            desc="down",
        )
        while True:
            scan_args = dict(TableName="hashes")

            if LastEvaluatedKey is not None:
                scan_args["ExclusiveStartKey"] = LastEvaluatedKey

            one_page_of_data = ddb_client.scan(**scan_args)

            self._ingest_one_page_from_dynamo(one_page_of_data)
            progress_bar.update(one_page_of_data["Count"])

            LastEvaluatedKey = one_page_of_data.get("LastEvaluatedKey")
            if LastEvaluatedKey is None:
                break

        self.stdout.write(f"{self.created_count=} {self.already_existed_count=}")

    def handle(self, *args, **options):
        self.stdout.write("Hello? *thump* *thump* Is this thing on?")
        TableName = "hashes"
        ddb_client = boto3.client(service_name="dynamodb")

        self.download(
            ddb_client=ddb_client,
            TableName=TableName,
        )

        # Now upload those items that we have but that aren't in dynamo.
        self.stdout.write(f"{len(self.hashes_in_dynamo)=}")
        need_uploading = ShortenedURL.objects.exclude(short__in=self.hashes_in_dynamo)
        self.stdout.write(f"{need_uploading.count()=}")
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(TableName)

        for item in tqdm.tqdm(
            need_uploading.all(),
            desc="up",
        ):
            create_date = item.created_at.isoformat()
            create_day = create_date[0:10]
            kwargs = dict(
                Item={
                    "create_date": create_date,
                    "create_day": create_day,
                    "long_url": item.original,
                    "human_hash": item.short,
                },
                ConditionExpression="attribute_not_exists(human_hash)",
            )

            try:
                table.put_item(**kwargs)
            except ClientError as e:
                if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                    pass
                else:
                    raise

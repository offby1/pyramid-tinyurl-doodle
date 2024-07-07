import pathlib

import boto3
import tqdm
from app.models import ShortenedURL
from django.core.management.base import BaseCommand

__here__ = pathlib.Path(__file__).parent.resolve()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Hello? *thump* *thump* Is this thing on?")
        ddb_client = boto3.client(service_name="dynamodb")
        all_the_data = ddb_client.scan(TableName="hashes")
        for key, value in all_the_data.items():
            if key != "Items":
                self.stdout.write(f"{key=} {value=}")

        for item in tqdm.tqdm(all_the_data["Items"]):
            long_url = item["long_url"]["S"]
            create_date = item["create_date"]["S"]
            human_hash = item["human_hash"]["S"]
            existing = ShortenedURL.objects.filter(short=human_hash)
            if existing.exists():
                self.stderr.write(f"Skipping existing {existing.first()}")
            else:
                ShortenedURL.objects.create(
                    created_at=create_date,
                    original=long_url,
                    short=human_hash,
                )

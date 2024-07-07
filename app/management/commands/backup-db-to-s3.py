import json
import pathlib
import tempfile

import boto3
from django.core.management import call_command
from django.core.management.base import BaseCommand

__here__ = pathlib.Path(__file__).parent.resolve()


def choose_backup_name(data):
    newest_entry = max(data, key=lambda datum: datum["fields"]["created_at"])
    return f'tinyurl-through-{newest_entry["fields"]["created_at"]}'


class Command(BaseCommand):
    def handle(self, *args, **options):
        s3_client = boto3.client(service_name="s3")

        with tempfile.NamedTemporaryFile(mode="w+") as tf:
            call_command("dumpdata", "app", stdout=tf)
            tf.flush()
            tf.seek(0)
            to_be_backed_up = json.load(tf)

            s3_name = choose_backup_name(to_be_backed_up)

            s3_client.upload_file(tf.name, "tinyurl-data-backups", s3_name)

        # TODO, maybe: delete old backups
        self.stderr.write(f"Uploaded {len(to_be_backed_up)=} records to {s3_name=}")

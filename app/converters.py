from django.conf import settings


class HashConverter:
    """I must be kept in sync with .views._enhashify"""

    regex = f"[0-9a-zA-Z]{{{settings.HASH_LENGTH}}}"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value[0 : settings.HASH_LENGTH]

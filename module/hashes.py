import binascii
import hashlib


def long_url_to_short_string(long_url, database):
    if isinstance(long_url, str):
        long_url_bytes = long_url.encode('utf-8')
    elif isinstance(long_url, bytes):
        long_url_bytes = long_url
    else:
        raise Exception("{} doesn't seem to be a string, or a bytes".format(long_url))

    hash_object = hashlib.sha256(long_url_bytes)
    binary_hash = hash_object.digest()
    human_hash_bytes = binascii.b2a_base64(binary_hash)
    human_hash_bytes = human_hash_bytes.replace(b'+', b'').replace(b'/',
                                                                   b'')[:10]
    short = human_hash_bytes.decode('utf-8')
    database.save_or_update(short, long_url)
    return short


def lengthen_short_string(string, database):
    return database.lookup(string)

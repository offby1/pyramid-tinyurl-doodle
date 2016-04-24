import database


def get_one_o_them_boto_session_thingies():
    pass


class DynamoDB(database.DatabaseMeta):

    def __init__(self,
                 aws_credentials='Do i look like a passsword?!',
                 aws_region='us-west-2',
                 aws_service=None):
        self.session = get_one_o_them_boto_session_thingies()

    def save(self, key, value):
        self.session.put_item(key, value)

    def lookup(self, key):
        self.session.get_item(key)

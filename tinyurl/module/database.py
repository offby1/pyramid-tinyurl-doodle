import abc


class DatabaseMeta(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_or_update(self, key, value):
        """Like save, but only writes to the database if the key is not
        already present.

        """
        pass

    @abc.abstractmethod
    def lookup(self, input):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass

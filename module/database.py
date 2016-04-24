import abc


class DatabaseMeta(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, key, value):
        pass

    @abc.abstractmethod
    def lookup(self, input):
        pass

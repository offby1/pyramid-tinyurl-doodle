import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DatabaseMeta(object):
    @abc.abstractmethod
    def add_if_not_present(self, key, value):
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

from abc import ABC, abstractmethod
from collections import namedtuple
from contextlib import contextmanager
from typing import Optional

Entry = namedtuple("Entry", ["entry", "entry_type"])


class BaseException(Exception):
    pass


class NoSuchFile(BaseException):
    def __init__(self, path, cause: Optional[Exception] = None):
        super().__init__(f"No file at {path}")
        self._path = path
        self._cause = cause


class AbstractStore(ABC):
    """
    Interface for data stores.  Allows reading and writing file-like object by
    path.
    """

    @abstractmethod
    @contextmanager
    def open(self, path, mode, *args, **kwargs):
        """Context manager that provides a handle to a file-like object.
        Attempts to mimic the ``open`` built-in as much as possible.

        :param path: The (relative) location of the file backing the stream.
        :param mode: The open mode of for the file.

        :returns: A file-like object.
        """
        pass

    def read(self, path, mode="", **kwargs):
        """Convenience wrapper around ``open`` to open files in read mode."""
        return self.open(path, "r" + mode, **kwargs)

    def write(self, path, mode="", **kwargs):
        """Convenience wrapper around ``open`` to open files in write mode."""
        return self.open(path, "w" + mode, **kwargs)

    @abstractmethod
    def substore(self, path):
        """Create a substore whose root directory is ``path`` in the superstore."""
        pass

    def location(self, path=None):
        """Return a client accessible location of the file under path."""
        pass

    def list(self, path=None):
        """Return a handle of relative entries under path."""
        pass


Store = AbstractStore

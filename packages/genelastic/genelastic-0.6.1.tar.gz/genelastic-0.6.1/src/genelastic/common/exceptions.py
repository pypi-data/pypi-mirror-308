# pylint: disable=missing-module-docstring

class DBIntegrityError(Exception):
    """Represents an integrity error,
    raised when the database content does not match the expected data schema.
    """

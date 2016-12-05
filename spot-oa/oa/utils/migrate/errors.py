class MigrationError(Exception):
    pass

class ConfigurationError(MigrationError):
    """Exception raised for invalid configuration.

    Attributes:
        cause -- Why is this error being raised
        hint -- Provided help to user
    """

    def __init__(self, cause, hint):
        self.cause = cause
        self.hint = hint

class TransformationError(MigrationError):
    """Exception raised for errors while running a transformation.

    Attributes:
        transformation_name -- Name of the transformation that was running
        message -- explanation of the error
    """

    def __init__(self, transformation_name, message):
        self.transformation_name = transformation_name
        self.message = message

class MigrationRuntimeError(RuntimeError):
    pass

class TransformationRuntimeError(MigrationRuntimeError):
    """Exception raised for errors while running a transformation.

Attributes:
transformation_name -- Name of the transformation that was running
message -- explanation of the error
"""

    def __init__(self, transformation_name, message):
        self.transformation_name = transformation_name
        self.message = message

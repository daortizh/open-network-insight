from errors import TransformationError

class BasicTransformation(object):
    def __init__(self, config=None):
        self.config = config

    def get_banner(self):
        raise TransformationError(str(self.__class__), 'Missing banner implementation')

    def apply(self, data):
        pass

    def before_run(self, reader=None, writer=None):
        pass

    def after_run(self, reader=None, writer=None):
        pass

class FooPublisher:
    def __init__(self, config):
        self._format = config.get('format', '{}: {}')

    def send_score_event(self, type, data):
        print self._format.format(type, str(data))

from transformations.basic import BasicTransformation

class DebugTransformation(BasicTransformation):
    def get_banner(self):
        return "Debugging rows"

    def apply(self, data):
        print data

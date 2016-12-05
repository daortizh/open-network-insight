from transformations.basic import BasicTransformation

class DeleteColumnTransformation(BasicTransformation):
    def get_banner(self):
        banner = 'Delete columns:'

        for name in self.config:
            banner = '{}\n{}'.format(banner, name)

        return banner

    def apply(self, data):
        for old_header in self.config:
            if data.has_key(old_header): del data[old_header]

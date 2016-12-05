from transformations.basic import BasicTransformation

class AddColumnTransformation(BasicTransformation):
    def get_banner(self):
        banner = 'Add new columns:'

        for name, value in self.config.items():
            banner = '{}\n{} = {}'.format(banner, name, value)

        return banner

    def apply(self, data):
        for key, value in self.config.items():
            data[key] = value

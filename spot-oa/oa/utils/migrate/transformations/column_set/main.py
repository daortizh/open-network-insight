from transformations.basic import BasicTransformation

class SetColumnTransformation(BasicTransformation):
    def get_banner(self):
        banner = 'Set column values:'

        for name, value in self.config.items():
            banner = '{}\n{} = {}'.format(banner, name, value)

        return banner

    def apply(self, data):
        for key, value in self.config.items():
            if data.has_key(key): data[key] = value

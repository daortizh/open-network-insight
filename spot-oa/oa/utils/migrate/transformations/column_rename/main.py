from transformations.basic import BasicTransformation

class ColumnRenameTransformation(BasicTransformation):
    def get_banner(self):
        banner = 'Rename columns:'

        for old_name, new_name in self.config.items():
            banner = '{}\n{} => {}'.format(banner, old_name, new_name)

        return banner

    def apply(self, data):
        for old_header, new_header in self.config.items():
            tmp = data[old_header]
            data[new_header] = tmp
            del data[old_header]

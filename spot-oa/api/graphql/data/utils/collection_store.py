class CollectionStore:
    def __init__(self, pipeline, dates, directory, filename, store_cls):
        self.pipeline = pipeline
        self.dates = dates
        self.directory = directory
        self.filename = filename
        self.store_cls = store_cls

    def load(self):
        records = []
        for date in self.dates:
            store = self.store_cls(pipeline=self.pipeline, date=date, directory=self.directory, filename=self.filename)

            records.extend(store.load())

        return records

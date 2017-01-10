from pipeline_store import PipelineStore

class DatedStore(PipelineStore):
    def __init__(self, pipeline, date):
        super(DatedStore, self).__init__(pipeline)
        self.date = date

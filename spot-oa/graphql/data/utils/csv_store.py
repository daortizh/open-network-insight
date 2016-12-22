from os import path
import csv

from dated_store import DatedStore
from pipeline_store import PipelineStore

class CsvDatedStore(DatedStore):
    def __init__(self, pipeline, date, directory, filename):
        super(self.__class__,self).__init__(pipeline=pipeline, date=date)
        self.csvfile = date.strftime(path.join(PipelineStore.DATA_PATH, pipeline, directory, filename))

    def load(self):
        records = []

        if not path.isfile(self.csvfile):
            return records

        with open(self.csvfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append(row)

        return records

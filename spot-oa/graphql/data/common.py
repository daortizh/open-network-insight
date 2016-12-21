from datetime import datetime, timedelta

from utils.collection_store import CollectionStore
from utils.csv_store import CsvDatedStore

def load_data_from_dates(pipeline, dirpttr, filepttr, dates = []):
    return CollectionStore(
                            pipeline=pipeline,
                            dates=dates,
                            directory=dirpttr,
                            filename=filepttr,
                            store_cls=CsvDatedStore
    ).load()

def day_range(start_date, end_date):
    start_date = datetime.strptime('{} 00:00:00'.format(start_date), '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime('{} 23:59:59'.format(end_date), '%Y-%m-%d %H:%M:%S')

    if start_date>end_date:
        raise RuntimeError('Invalid date range')

    dates = []
    date = start_date
    while start_date<=date and date<=end_date:
        dates.append(date)

        date = date + timedelta(days=1)

    print dates
    return dates

def month_range(start_date, end_date):
    start_date = datetime.strptime('{} 00:00:00'.format(start_date), '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime('{} 23:59:59'.format(end_date), '%Y-%m-%d %H:%M:%S')

    if start_date>end_date:
        raise RuntimeError('Invalid date range')

    date = start_date
    dates = [start_date]
    while date.year<=start_date.year and date.month<end_date.month:
        if date.month==12:
            date = datetime(year=date.year+1, month=1, day=1)
        else:
            date = datetime(year=date.year, month=date.month+1, day=1)

        dates.append(date)

    return dates

def load_ingest_summary(pipeline, start_date, end_date):
    dates = month_range(start_date, end_date)

    records = load_data_from_dates(pipeline, 'ingest_summary', 'is_%Y%m.csv', dates)

    start_date = datetime.strptime('{} 00:00:00'.format(start_date), '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime('{} 23:59:59'.format(end_date), '%Y-%m-%d %H:%M:%S')

    return filter(lambda record : start_date<=datetime.strptime(record.get('date'), '%Y-%m-%d %H:%S') and datetime.strptime(record.get('date'), '%Y-%m-%d %H:%S')<=end_date, records)

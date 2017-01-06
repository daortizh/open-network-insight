from datetime import datetime, timedelta

from glima import get_raw_data, get_ingest_summary
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

def apply_filters(record, filters=[]):
    state = None
    for key, value, chain in filters:
        partial_state = record.get(key, '') == value

        if state is None:
            state = partial_state
        elif chain=='and':
            state = state and partial_state
        else:
            state = state or partial_state

    return state or False

def load_suspicious(pipeline, ip, start_date, end_date):
    dates = day_range(start_date, end_date)

    if ip is not None:
        filters = (('srcIP', ip, 'or'),('dstIP', ip, 'or'),('sev', '0', 'and'))
    else:
        filters = (('sev', '0', 'and'),)

    records = load_data_from_dates(pipeline, '%Y%m%d', '{}_scores.csv'.format(pipeline), day_range(start_date, end_date))[0:250]

    if filters is not None:
        return filter(lambda record : apply_filters(record, filters), records)
    else:
        return records

def load_ingest_summary(pipeline, start_date, end_date):
    start_date = datetime.strptime('{}'.format(start_date), '%Y-%m-%d')
    end_date = datetime.strptime('{}'.format(end_date), '%Y-%m-%d')

    print (
        'is.{}'.format(pipeline),
        start_date.year, start_date.month, start_date.day,
        end_date.year, end_date.month, end_date.day
    )
    is_data = get_ingest_summary(
        pipeline,
        start_date.year, start_date.month, start_date.day,
        end_date.year, end_date.month, end_date.day,
        200
    )
    print 'Back from query'

    return is_data

def load_raw_data(pipeline, start_date, end_date):
    start_date = datetime.strptime('{}'.format(start_date), '%Y-%m-%d')
    end_date = datetime.strptime('{}'.format(end_date), '%Y-%m-%d')

    print (
        'rd.{}'.format(pipeline),
        start_date.year, start_date.month, start_date.day,
        end_date.year, end_date.month, end_date.day
    )
    raw_data = get_raw_data(
        pipeline,
        start_date.year, start_date.month, start_date.day,
        end_date.year, end_date.month, end_date.day,
        20000
    )
    print 'Back from query'

    return raw_data

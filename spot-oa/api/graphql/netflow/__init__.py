from datetime import datetime
from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLList,
    GraphQLString
)

from data.common import day_range, load_data_from_dates, load_suspicious, load_ingest_summary, load_raw_data
from data.utils.csv_store import CsvDatedStore

from raw import RawDataType
from suspicious import SuspiciousType
from details import DetailsType
from shared.ingest_summary import IngestSummaryType

def get_date_range(args):
    date = args.get('date', datetime.now().strftime('%Y-%m-%d'))
    start_date = args.get('startDate', date)
    end_date = args.get('endDate', start_date)

    return (start_date, end_date)

NetflowType = GraphQLObjectType(
  name = 'NetflowType',
  fields = {
    'suspicious': GraphQLField(
        type=GraphQLList(SuspiciousType),
        args={
            'date': GraphQLArgument(
                type=GraphQLString
            ),
            'startDate': GraphQLArgument(
                type=GraphQLString
            ),
            'endDate': GraphQLArgument(
                type=GraphQLString
            ),
            'ip': GraphQLArgument(
                type=GraphQLString
            )
        },
        resolver=lambda root, args, *_ : load_suspicious('flow', args.get('ip', None), *get_date_range(args))
    ),
    'details': GraphQLField(
        type=GraphQLList(DetailsType),
        args={
            'date': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString)
            ),
            'srcIp': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString)
            ),
            'dstIp': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString)
            ),
            'time': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString)
            )
        },
        resolver=lambda root, args, *_ : CsvDatedStore('flow', datetime.strptime(args.get('date'), '%Y-%m-%d'), '%Y%m%d', 'edge-{}-{}-{}.tsv'.format(args.get('srcIp').replace('.', '_'), args.get('dstIp').replace('.', '_'), args.get('time').replace(':', '-')), delimiter='\t').load()
    ),
    'ingestSummary': GraphQLField(
        type=GraphQLList(IngestSummaryType),
        args={
            'startDate': GraphQLArgument(
                type=GraphQLString
            ),
            'endDate': GraphQLArgument(
                type=GraphQLString
            )
        },
        resolver=lambda root, args, *_ : load_ingest_summary('flow', *get_date_range(args))
    ),
    'raw': GraphQLField(
        type=GraphQLList(RawDataType),
        args={
            'startDate': GraphQLArgument(
                type=GraphQLString
            ),
            'endDate': GraphQLArgument(
                type=GraphQLString
            )
        }
    )
  }
)

from datetime import datetime
from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLList,
    GraphQLString
)

from data.common import day_range, load_data_from_dates, load_ingest_summary
from suspicious import SuspiciousType
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
            )
        },
        resolver=lambda root, args, *_ : load_data_from_dates('flow', '%Y%m%d', 'flow_scores.csv', day_range(*get_date_range(args)))
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
    )
  }
)

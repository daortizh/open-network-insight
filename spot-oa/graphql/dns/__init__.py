from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLList,
    GraphQLString
)

from data.common import load_ingest_summary
from shared.ingest_summary import IngestSummaryType

DnsType = GraphQLObjectType(
  name = 'DnsType',
  fields = {
    'ingestSummary': GraphQLField(
        type=GraphQLList(IngestSummaryType),
        args={
            'startDate': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString)
            ),
            'endDate': GraphQLArgument(
                type=GraphQLNonNull(GraphQLString)
            )
        },
        resolver=lambda root, args, *_ : load_ingest_summary('dns', args.get('startDate'), args.get('endDate'))
    )
  }
)

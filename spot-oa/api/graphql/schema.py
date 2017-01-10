from graphql import (
    GraphQLArgument,
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField
)

from netflow import NetflowType
from dns import DnsType
from proxy import ProxyType

QueryType = GraphQLObjectType(
    name = 'RootQueryType',
    fields = {
        'netflow': GraphQLField(
            type=NetflowType,
            resolver=lambda *_: {}
        ),
        'dns': GraphQLField(
            type=DnsType,
            resolver=lambda *_: {}
        ),
        'proxy': GraphQLField(
            type=ProxyType,
            resolver=lambda *_: {}
        )
  }
)

from netflow.mutation import ScoreInputType, ScoreOutputType

def score_netflow(root, args, *_):
    publish_score_event('netflow', args.get('input'))

    return True

from api.integrators import publish_score_event

MutationType = GraphQLObjectType(
    name = 'RootMutationType',
    fields = {
        'scoreNetflow': GraphQLField(
            type=ScoreOutputType,
            args={
                'input': GraphQLArgument(
                    type=ScoreInputType
                )
            },
            resolver=score_netflow
        )
    }
)

schema = GraphQLSchema(
  query = QueryType,
  mutation = MutationType
)

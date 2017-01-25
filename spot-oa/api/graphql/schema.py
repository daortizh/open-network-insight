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

from netflow.mutation import ScoreInputType, DxlTagInputType, DxlOutputType

def score_netflow(root, args, *_):
    publish_score_event('netflow', args.get('input'))

    return True

from api.integrators import publish_score_event, publish_tag_device

def tag_device(root, args, *_):
    publish_tag_device(args.get('input'))

    return True

MutationType = GraphQLObjectType(
    name = 'RootMutationType',
    fields = {
        'scoreNetflow': GraphQLField(
            type=DxlOutputType,
            args={
                'input': GraphQLArgument(
                    type=ScoreInputType
                )
            },
            resolver=score_netflow
        ),
        'tagDevice': GraphQLField(
            type=DxlOutputType,
            args={
                'input': GraphQLArgument(
                    type=DxlTagInputType
                )
            },
            resolver=tag_device
        )
    }
)

schema = GraphQLSchema(
  query = QueryType,
  mutation = MutationType
)

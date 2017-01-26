from graphql import (
    GraphQLArgument,
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLList
)

from netflow import NetflowType
from dns import DnsType
from proxy import ProxyType

from mar import MarType

from api.integrators import publish_score_event, publish_tag_device, request_device_info

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
        ),
        'mar': GraphQLField(
            type=GraphQLList(MarType),
            args={
                'ip': GraphQLArgument(
                    type=GraphQLString
                )
            },
            resolver=lambda root, args, *_ : request_device_info(args.get('ip'))
        )
    }
)

from netflow.mutation import ScoreInputType, DxlTagInputType, DxlOutputType

def score_netflow(root, args, *_):
    publish_score_event('netflow', args.get('input'))

    return True

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

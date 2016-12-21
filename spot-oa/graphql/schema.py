from graphql import (
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

schema = GraphQLSchema(
  query= QueryType
)

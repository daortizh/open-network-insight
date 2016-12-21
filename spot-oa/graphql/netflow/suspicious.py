from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLInt
)

SuspiciousType = GraphQLObjectType(
    name = 'NetflowSuspiciousType',
    fields = {
        'timestamp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_: root.get('tstart')
        ),
        'srcIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('srcIP')
        ),
        'dstIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('dstIP')
        ),
        'srcPort': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('sport')
        ),
        'dstPort': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('dport')
        )
    }
)

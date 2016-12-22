from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLInt
)

DetailsType = GraphQLObjectType(
    name = 'NetflowDetailsType',
    fields = {
        'tstart': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_: root.get('tstart')
        ),
        'srcIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('srcip')
        ),
        'srcPort': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('sport') or 0
        ),
        'dstIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('dstip')
        ),
        'dstPort': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('dport') or 0
        ),
        'protocol': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('proto')
        ),
        'flags': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('flags')
        ),
        'tos': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('tos')
        ),
        'inPkts': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('ipkts') or 0
        ),
        'inBytes': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('ibytes') or 0
        ),
        'outPkts': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('opkts') or 0
        ),
        'outBytes': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('obytes') or 0
        ),
        'routerIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('rip')
        ),
        'inIface': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('input')
        ),
        'outIface': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('output')
        )
    }
)

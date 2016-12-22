from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLInt,
    GraphQLFloat
)

SuspiciousType = GraphQLObjectType(
    name = 'NetflowSuspiciousType',
    fields = {
        'rank': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_: root.get('rank') or 0
        ),
        'tstart': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_: root.get('tstart')
        ),
        'srcIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('srcIP')
        ),
        'srcPort': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('sport') or 0
        ),
        'srcIpInternal': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('srcIpInternal') or 0
        ),
        'srcIpRep': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('srcIP_rep')
        ),
        'dstIp': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('dstIP')
        ),
        'dstPort': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('dport') or 0
        ),
        'dstIpInternal': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('destIpInternal') or 0
        ),
        'dstIpRep': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('dstIP_rep')
        ),
        'protocol': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('proto')
        ),
        'inPkts': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('ipkt') or 0
        ),
        'inBytes': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('ibyt') or 0
        ),
        'outPkts': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('opkt') or 0
        ),
        'outBytes': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('obyt') or 0
        ),
        'score': GraphQLField(
            type=GraphQLFloat,
            resolver=lambda root, *_ : root.get('score') or 0.0
        ),
        'sev': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('sev') or 0
        )
    }
)

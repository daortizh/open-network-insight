from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLInt,
    GraphQLFloat
)

RawDataType = GraphQLObjectType(
    name = 'NetflowRawDataType',
    fields = {
        'treceived': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('treceived')
        ),
        'unix_tstamp': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('unix_tstamp') or 0
        ),
        'tryear': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('tryear') or 0
        ),
        'trmonth': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('trmonth') or 0
        ),
        'trday': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('trday') or 0
        ),
        'trhour': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('trhour') or 0
        ),
        'trminute': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('trminute') or 0
        ),
        'trsec': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('trsec') or 0
        ),
        'tdur': GraphQLField(
            type=GraphQLFloat,
            resolver=lambda root, *_ : root.get('tdur') or 0
        ),
        'sip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('sip')
        ),
        'dip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('dip')
        ),
        'sport': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('sport') or 0
        ),
        'dport': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('dport') or 0
        ),
        'proto': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('proto')
        ),
        'flag': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('flag')
        ),
        'fwd': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('fwd') or 0
        ),
        'stos': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('stos') or 0
        ),
        'ipkt': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('ipkt') or 0
        ),
        'ibyt': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('ibyt') or 0
        ),
        'opkt': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('opkt') or 0
        ),
        'obyt': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('obyt') or 0
        ),
        'input': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('input') or 0
        ),
        'output': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('output') or 0
        ),
        'sas': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('sas') or 0
        ),
        'das': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('das') or 0
        ),
        'dtos': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('dtos') or 0
        ),
        'dir': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, *_ : root.get('dir') or 0
        ),
        'rip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, *_ : root.get('rip')
        )
    }
)

from graphql import (
    GraphQLString,
    GraphQLInt,
    GraphQLObjectType,
    GraphQLField
)

MarCurrentFlowType = GraphQLObjectType(
    name = 'MarCurrentFlowType',
    fields = {
        'local_ip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|local_ip')
        ),
        'local_port': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|local_port')
        ),
        'remote_ip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|remote_ip')
        ),
        'remote_port': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|remote_port')
        ),
        'status': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|status')
        ),
        'user_id': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|user_id')
        ),
        'user': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('CurrentFlow|user')
        )
    }
)

MarNetworkFlowType = GraphQLObjectType(
    name = 'MarNetworkFlowType',
    fields = {
        'time': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|time')
        ),
        'direction': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|direction')
        ),
        'src_ip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|src_ip')
        ),
        'src_port': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|src_port')
        ),
        'dst_ip': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|dst_ip')
        ),
        'dst_port': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|dst_port')
        ),
        'status': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|status')
        ),
        'proto': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|proto')
        ),
        'process': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|process')
        ),
        'user': GraphQLField(
            type=GraphQLString,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|user')
        ),
        'count': GraphQLField(
            type=GraphQLInt,
            resolver=lambda root, args, *_ : root.get('NetworkFlow|count')
        )
    }
)

MarType = GraphQLObjectType(
    name = 'MarType',
    fields = {
        'CurrentFlow': GraphQLField(
            type=MarCurrentFlowType,
            resolver=lambda root, args, *_ : root
        ),
	'NetworkFlow': GraphQLField(
	    type=MarNetworkFlowType,
            resolver=lambda root, args, *_ : root
        )
    }
)

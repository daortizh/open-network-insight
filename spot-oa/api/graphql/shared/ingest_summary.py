from graphql import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLString,
    GraphQLInt
)

IngestSummaryType = GraphQLObjectType(
    name = 'IngestSummaryType',
    fields = {
        'date': GraphQLField(
            type = GraphQLNonNull(GraphQLString),
            resolver=lambda root, *_: '{}-{:02d}-{:02d} {:02d}:{:02d}'.format(
		root.get('tryear'),
		root.get('trmonth'),
		root.get('trday'),
		root.get('trhour'),
		root.get('trminute')
            )
        ),
        'total': GraphQLField(
            type = GraphQLNonNull(GraphQLInt),
            resolver=lambda root, *_:root.get('total', 0)
        )
    }
)

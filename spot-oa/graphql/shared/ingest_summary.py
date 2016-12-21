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
            resolver=lambda root, *_:root.get('date')
        ),
        'total': GraphQLField(
            type = GraphQLNonNull(GraphQLInt),
            resolver=lambda root, *_:root.get('total', 0)
        )
    }
)

from collections import OrderedDict

from graphql import (
    GraphQLArgument,
    GraphQLBoolean,
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInputObjectField,
    GraphQLField,
    GraphQLObjectType,
    GraphQLString,
    GraphQLInt
)

from graphql.type import GraphQLEnumValue

ScoreType = GraphQLEnumType(
    name='ScoreType',
    values=OrderedDict((
        ('HIGH', GraphQLEnumValue(1)),
        ('MEDIUM', GraphQLEnumValue(value=2)),
        ('LOW', GraphQLEnumValue(value=3))
    ))
)

ScoreInputType = GraphQLInputObjectType(
    name='NetflowScoreInputType',
    fields={
        'srcIp': GraphQLInputObjectField(
            type=GraphQLString
        ),
        'srcPort': GraphQLInputObjectField(
            type=GraphQLInt
        ),
        'dstIp': GraphQLInputObjectField(
            type=GraphQLString
        ),
        'dstPort': GraphQLInputObjectField(
            type=GraphQLInt
        ),
        'score': GraphQLInputObjectField(
            type=ScoreType
        )
    }
)

ScoreOutputType = GraphQLObjectType(
    name='NetflowScoreOutputType',
    fields={
        'success': GraphQLField(
            type=GraphQLBoolean
        )
    }
)

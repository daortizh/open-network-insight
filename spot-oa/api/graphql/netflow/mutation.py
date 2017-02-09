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

DxlOutputType = GraphQLObjectType(
    name='NetflowDxlOutputType',
    fields={
        'success': GraphQLField(
            type=GraphQLBoolean
        )
    }
)

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

DxlTagType = GraphQLEnumType(
    name='DxlTagType',
    values=OrderedDict((
        ('BLOCK', GraphQLEnumValue('BLOCK')),
        ('QUARANTINE', GraphQLEnumValue(value='QUARANTINE')),
        ('MARINSTALL', GraphQLEnumValue(value='MARINSTALL'))
    ))
)

DxlTagInputType = GraphQLInputObjectType(
    name='DxlTagInputType',
    fields={
        'srcIp': GraphQLInputObjectField(
            type=GraphQLString
        ),
        'dstIp': GraphQLInputObjectField(
            type=GraphQLString
        ),
        'target': GraphQLInputObjectField(
            type=GraphQLString
        ),
        'tag': GraphQLInputObjectField(
            type=DxlTagType
        )
    }
)

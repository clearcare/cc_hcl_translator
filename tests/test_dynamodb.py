from __future__ import unicode_literals

import os

from hcl_translator import dynamodb_translator
from moto import mock_dynamodb

AWS_DYNAMODB_TF_PATH = os.path.join(os.path.dirname(__file__), 'dynamo_tables.tf')

dynamodb_table_info = dynamodb_translator(AWS_DYNAMODB_TF_PATH)


@mock_dynamodb
def test_get_table_info_schema():

    table_info = dynamodb_table_info.get_table_info('change_in_condition')
    assert table_info['schema'][0].definition() == {
        'AttributeName': 'carelog_id',
        'AttributeType': 'N',
    }

    assert table_info['schema'][0].schema() == {
        'KeyType': 'HASH',
        'AttributeName': 'carelog_id',
    }


@mock_dynamodb
def test_get_table_info_indexes():

    table_info = dynamodb_table_info.get_table_info('change_in_condition')
    assert table_info['indexes'][0].definition() == [
        {
            'AttributeName': 'carelog_id',
            'AttributeType': 'N',
        },
        {
            'AttributeName': 'session_id',
            'AttributeType': 'N',
        }
    ]

    assert table_info['indexes'][0].schema() == {
        'KeySchema': [
            {
                'KeyType': 'HASH',
                'AttributeName': 'carelog_id',
            },
            {
                'KeyType': 'RANGE',
                'AttributeName': 'session_id',
            }
        ],
        'IndexName': 'SessionId',
        'Projection': {
            'ProjectionType': 'ALL',
        },
    }


@mock_dynamodb
def test_get_table_info_global_indexes():

    table_info = dynamodb_table_info.get_table_info('change_in_condition')
    assert table_info['global_indexes'][0].definition() == [
        {
            'AttributeName': 'saved_in_rdb',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'time',
            'AttributeType': 'N',
        }
    ]

    assert table_info['global_indexes'][0].schema() == {
        'KeySchema': [
            {
                'KeyType': 'HASH',
                'AttributeName': 'saved_in_rdb',
            },
            {
                'KeyType': 'RANGE',
                'AttributeName': 'time',
            }
        ],
        'IndexName': 'SavedInRDB',
        'Projection': {
            'ProjectionType': 'ALL',
        },
        'ProvisionedThroughput': {
            'WriteCapacityUnits': 5,
            'ReadCapacityUnits': 5,
        }
    }

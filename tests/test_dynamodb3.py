from __future__ import unicode_literals

import os

from hcl_translator import dynamodb3_translator
from moto import mock_dynamodb

AWS_DYNAMODB_TF_PATH = os.path.join(os.path.dirname(__file__), 'dynamo_tables.tf')

dynamodb3_table_info = dynamodb3_translator(AWS_DYNAMODB_TF_PATH)


@mock_dynamodb
def test_get_table_info_key_schema():

    table_info = dynamodb3_table_info.get_table('change_in_condition')
    assert table_info['KeySchema'] == [
        {
            "KeyType": "HASH",
            "AttributeName": "carelog_id",
        },
        {
            "KeyType": "RANGE",
            "AttributeName": "time",
        }
    ]


@mock_dynamodb
def test_get_table_info_indexes():

    table_info = dynamodb3_table_info.get_table('change_in_condition')
    assert table_info["LocalSecondaryIndexes"] == [
        {
            "KeySchema": [
                {
                    "KeyType": "HASH",
                    "AttributeName": "carelog_id",
                },
                {
                    "KeyType": "RANGE",
                    "AttributeName": "session_id",
                }
            ],
            "IndexName": "SessionId",
            "Projection": {
                "ProjectionType": "ALL",
            }
        },
        {
            "KeySchema": [
                {
                    "KeyType": "HASH",
                    "AttributeName": "agency_id",
                },
                {
                    "KeyType": "RANGE",
                    "AttributeName": "caregiver_id",
                }
            ],
            "IndexName": "CaregiverId",
            "Projection": {
                "ProjectionType": "ALL",
            }
         },
    ]


@mock_dynamodb
def test_get_table_info_global_indexes():
    import json
    table_info = dynamodb3_table_info.get_table('change_in_condition')
    print(json.dumps(table_info["GlobalSecondaryIndexes"], indent=4))
    assert table_info["GlobalSecondaryIndexes"] == [
        {
            "KeySchema": [
                {
                    "KeyType": "HASH",
                    "AttributeName": "saved_in_rdb",
                },
                {
                    "KeyType": "RANGE",
                    "AttributeName": "time",
                },
            ],
            "IndexName": "SavedInRDB",
            "Projection": {
                "ProjectionType": "ALL",
            },
            "ProvisionedThroughput": {
                "WriteCapacityUnits": 15,
                "ReadCapacityUnits": 15
            }
        },
        {
            "KeySchema": [
                {
                    "KeyType": "HASH",
                    "AttributeName": "an_attribute",
                },
                {
                    "KeyType": "RANGE",
                    "AttributeName": "another_attribute",
                },
            ],
            "IndexName": "AnotherIndex",
            "Projection": {
                "ProjectionType": "ALL",
            },
            "ProvisionedThroughput": {
                "WriteCapacityUnits": 15,
                "ReadCapacityUnits": 15
            }
        }
    ]


@mock_dynamodb
def test_get_table_info_attribute_definitions():
    import json
    table_info = dynamodb3_table_info.get_table('change_in_condition')
    print(json.dumps(table_info["AttributeDefinitions"], indent=4))
    assert table_info["AttributeDefinitions"] == [
        {
            "AttributeName": "carelog_id",
            "AttributeType": "N",
        },
        {
            "AttributeName": "time",
            "AttributeType": "N",
        },
        {
            "AttributeName": "saved_in_rdb",
            "AttributeType": "N",
        },
        {
            "AttributeName": "session_id",
            "AttributeType": "N",
        },
        {
            "AttributeName": "an_attribute",
            "AttributeType": "N"
        },
        {
            "AttributeName": "another_attribute",
            "AttributeType": "N"
        },
        {
            "AttributeName": "agency_id",
            "AttributeType": "N"
        },
        {
            "AttributeName": "caregiver_id",
            "AttributeType": "N"
        }
    ]

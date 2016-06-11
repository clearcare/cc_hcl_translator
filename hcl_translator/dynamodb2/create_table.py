from __future__ import absolute_import

from hcl_translator.base import BaseDynamodbTranslator
from hcl_translator.exceptions import UnknownTableException


class Dynamodb2CreateTableTranslator(BaseDynamodbTranslator):

    def _translate_projection_key(self, projection_key, is_global=False):
        return '{}{}Index'.format('Global' if is_global else '', projection_key.title())

    def _translate_field_type(self, field_type):
        return ''.join(c.title() for c in field_type.split('_'))

    def _translate_attributes(self, attributes):
        return [
            {
                'AttributeName': attribute['name'],
                'AttributeType': attribute['type']
            } for attribute in attributes
        ]

    def _translate_schema(self, key_config):
        schema = []
        hash_key = key_config.get('hash_key')
        if hash_key:
            schema.append(
                {
                    'AttributeName': hash_key,
                    'KeyType': 'HASH',
                }
            )

        range_key = key_config.get('range_key')
        if range_key:
            schema.append(
                {
                    'AttributeName': range_key,
                    'KeyType': 'RANGE',
                }
            )
        return schema

    def _translate_index_kwargs(self, index_details, attributes):
        kwargs = {'parts': []}
        hash_key = index_details.get('hash_key')
        if hash_key:
            kwargs['parts'].append(
                self._translate_attribute(hash_key, 'hash_key', attributes),
            )
        range_key = index_details.get('range_key')
        if range_key:
            kwargs['parts'].append(
                self._translate_attribute(range_key, 'range_key', attributes)
            )
        return kwargs

    def _translate_index(self, index):
        schema = {
            'IndexName': index['name'],
            'KeySchema': self._translate_schema(index),
        }
        projection_type = index.get('projection_type')
        if projection_type:
            schema['Projection'] = {
                'ProjectionType': projection_type
            }
        return schema

    def _translate_indexes(self, indexes):

        if not isinstance(indexes, (list, tuple)):
            indexes = [indexes]
        return [
            self._translate_index(index_details) for index_details in indexes
        ]

    def create_table_args(self, table_name, namespace):

        try:
            table = self.terraform_config['resource']['aws_dynamodb_table'][table_name]
        except KeyError:
            raise UnknownTableException('Unknown table: %s' % table_name)

        args = [
            self._translate_attributes(table['attribute']),
            namespace + table_name,
            self._translate_schema(table),
            # These are placeholders and never used.
            {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            }
        ]

        kwargs = {}

        global_secondary_index = table.get('global_secondary_index')
        if global_secondary_index is not None:
            kwargs['global_secondary_indexes'] = self._translate_indexes(global_secondary_index)

        local_secondary_index = table.get('local_secondary_index')
        if local_secondary_index is not None:
            kwargs['local_secondary_indexes'] = self._translate_indexes(local_secondary_index)

        return args, kwargs

dynamodb2_create_table_translator = Dynamodb2CreateTableTranslator

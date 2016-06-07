from .base import BaseDynamodbTranslator
from .exceptions import UnknownTableException


class Dynamodb3Translator(BaseDynamodbTranslator):

    def _translate_key_schema(self, table_data):
        attributes = [
            {
                "KeyType": "HASH",
                "AttributeName": table_data['hash_key'],
            }
        ]

        range_key = table_data.get('range_key')
        if range_key:
            attributes.append({
                "KeyType": "RANGE",
                "AttributeName": range_key,
            })

        return attributes

    def _translate_attribute_definitions(self, table_data):
        attributes = table_data['attribute']
        if not isinstance(attributes, list):
            attributes = [attributes]
        return [
            {
                'AttributeName': attribute['name'],
                'AttributeType': attribute['type'],
            } for attribute in attributes
        ]

    def _translate_index(self, indexes):
        translated = []
        if not isinstance(indexes, (list, tuple)):
            indexes = [indexes]

        for index_data in indexes:
            attributes = {
                'KeySchema': self._translate_key_schema(index_data),
            }
            attributes['IndexName'] = index_data['name']
            attributes['Projection'] = {
                'ProjectionType': index_data['projection_type'].upper(),
            }

            read_capacity = index_data.get('read_capacity')
            write_capacity = index_data.get('write_capacity')
            if read_capacity and write_capacity:
                attributes['ProvisionedThroughput'] = {
                    'ReadCapacityUnits': int(read_capacity),
                    'WriteCapacityUnits': int(write_capacity)
                }
            translated.append(attributes)
        return translated

    def get_table(self, table_name):
        try:
            table_data = self.terraform_config['resource']['aws_dynamodb_table'][table_name]
        except KeyError:
            raise UnknownTableException('Unknown table: %s' % table_name)

        metadata = {
            'KeySchema': self._translate_key_schema(table_data),
            'AttributeDefinitions': self._translate_attribute_definitions(table_data),
        }

        global_indexes_config = table_data.get('global_secondary_index')
        if global_indexes_config is not None:
            metadata['GlobalSecondaryIndexes'] = self._translate_index(global_indexes_config)

        indexes_config = table_data.get('local_secondary_index')
        if indexes_config is not None:
            metadata['LocalSecondaryIndexes'] = self._translate_index(indexes_config)

        return metadata

dynamodb3_translator = Dynamodb3Translator

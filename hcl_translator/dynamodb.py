from boto.dynamodb2 import fields

from .base import BaseDynamodbTranslator
from .exceptions import UnknownTableException


class DynamodbTranslator(BaseDynamodbTranslator):

    def _translate_projection_key(self, projection_key, is_global=False):
        return '{}{}Index'.format('Global' if is_global else '', projection_key.title())

    def _translate_field_type(self, field_type):
        return ''.join(c.title() for c in field_type.split('_'))

    def _translate_attributes(self, attributes):
        return {attribute['name']: attribute['type'] for attribute in attributes}

    def _translate_attribute(self, field_name, field_type, attributes):
        key_type = getattr(fields, self._translate_field_type(field_type))
        return key_type(field_name, **{'data_type': attributes[field_name]})

    def _translate_schema(self, key_config, attributes):
        hash_key = key_config['hash_key']
        schema = [
            self._translate_attribute(hash_key, 'hash_key', attributes)
        ]

        range_key = key_config.get('range_key')
        if range_key:
            schema.append(self._translate_attribute(range_key, 'range_key', attributes))
        return schema

    def _translate_index_kwargs(self, index_details, attributes):
        kwargs = {
            'parts': [],
        }
        hash_key = index_details.get('hash_key')
        if hash_key:
            kwargs['parts'].append(
                self._translate_attribute(hash_key, 'hash_key', attributes),
            )
        range_key = index_details.get('range_key')
        if range_key:
            kwargs['parts'].append(
                self._translate_attribute(range_key, 'range_key', attributes),
            )
        return kwargs

    def _translate_index(self, index, attributes, is_global=False):
        index_type = getattr(
            fields,
            self._translate_projection_key(index['projection_type'], is_global=is_global)
        )
        kwargs = self._translate_index_kwargs(index, attributes)
        return index_type(index['name'], **kwargs)

    def _translate_indexes(self, indexes, attributes, is_global=False):
        if not isinstance(indexes, (list, tuple)):
            indexes = [indexes]
        translated = []
        for index_details in indexes:
            translated.append(
                self._translate_index(index_details, attributes, is_global)
            )
        return translated

    def get_table(self, table_name):

        try:
            table = self.terraform_config['resource']['aws_dynamodb_table'][table_name]
        except KeyError:
            self.logger.exception('cc_dynamodb.UnknownTable', extra=dict(
                table_name=table_name,
                table=table_name,
                DTM_EVENT='cc_dynamodb.UnknownTable'),
            )
            raise UnknownTableException('Unknown table: %s' % table_name)

        attributes = self._translate_attributes(table['attribute'])

        metadata = {
            'schema': self._translate_schema(table, attributes),
        }

        global_secondary_index = table.get('global_secondary_index')
        if global_secondary_index is not None:
            metadata['global_indexes'] = self._translate_indexes(global_secondary_index, attributes, is_global=True)

        local_secondary_index = table.get('local_secondary_index')
        if local_secondary_index is not None:
            metadata['indexes'] = self._translate_indexes(local_secondary_index, attributes)

        return metadata

dynamodb_translator = DynamodbTranslator

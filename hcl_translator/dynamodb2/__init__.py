from __future__ import absolute_import

from .create_table import dynamodb2_create_table_translator
from .table import dynamodb2_table_translator


class Dynamodb2Translator(object):
    """
    Just thin wrapper to combine dynamodb2_table_translator and
    dynamodb2_create_table_translator.
    """
    def __init__(self, dynamodb_tf, logger):
        self.dynamodb_tf = dynamodb_tf
        self.logger = logger

        self.create_table_translator = dynamodb2_create_table_translator(self.dynamodb_tf, self.logger)
        self.table_translator = dynamodb2_table_translator(self.dynamodb_tf, self.logger)

    def create_table_args(self, table_name, namespace):
        return self.create_table_translator.create_table_args(table_name, namespace)

    def table_kwargs(self, table_name):
        return self.table_translator.table_kwargs(table_name)

    def get_table_index(self, table_name, index_name):
        return self.table_translator.get_table_index(table_name, index_name)

    def list_table_names(self):
        return self.table_translator.list_table_names()

dynamodb2_translator = Dynamodb2Translator

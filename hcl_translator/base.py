import hcl
import logging


class BaseDynamodbTranslator(object):

    def __init__(self, dynamodb_tf, logger=None):
        self.dynamodb_tf = dynamodb_tf
        self.logger = logger or logging.getLogger(__file__)
        self._terraform_config = None

    @property
    def terraform_config(self):
        if self._terraform_config is None:
            with open(self.dynamodb_tf) as hcl_file:
                self._terraform_config = hcl.load(hcl_file)
        return self._terraform_config

    def get_table_index(self, table_name, index_name):
        for table_name, table_data in self.terraform_config['resource']['aws_dynamodb_table'].iteritems():
            for field, value in table_data.iteritems():
                if field.endswith('index'):
                    index_data = table_data[field]
                    if index_data['name'] == index_name:
                        attributes = self._translate_attributes(table_data['attribute'])
                        return self._translate_index(
                              index_data, attributes, False if field.startswith('local') else True)

    def list_table_names(self):
        return self.terraform_config['resource']['aws_dynamodb_table'].keys()

    def get_table(self, table_name):
        raise NotImplemented

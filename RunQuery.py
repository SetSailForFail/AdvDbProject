from PropertyTableHelper import PropertiesHelper
from AlgorithmsHelper import Algorithm


def run_query(file_path, dict_path, algo, yannakis, output_file):

    properties = {'follows', 'friendOf', 'likes', 'hasReview'}
    tables = PropertiesHelper(file_path, dict_path, properties).tables
    Algorithm(algo, yannakis, tables, output_file)
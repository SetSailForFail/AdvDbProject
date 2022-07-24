from PropertyTableHelper import PropertiesHelper
from AlgorithmsHelper import Algorithm


def run_query(file_path, algo, yannakis, output_file):

    properties = {'follows', 'friendOf', 'likes', 'hasReview'}
    property_helper = PropertiesHelper(file_path, properties)
    Algorithm(algo, yannakis, property_helper, output_file)
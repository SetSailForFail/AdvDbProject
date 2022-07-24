from collections import defaultdict

class PropertiesHelper:

    def __init__(self, file_path, properties):

        self.tables = {property_name: defaultdict(list) for property_name in properties}
        self.rdf_dict = defaultdict()
        self.rdf_dict_reversed = defaultdict()
        self.get_property_tables(file_path)
        self.reverse_rdf_dict()


    def get_property_tables(self, file_path):
        """
        populates each property table (given by properties in the constructor) with object being the index
        and the corresponding subjects the values of that index
        """
        with open (file_path, 'r') as file:

            for line in file:

                subj, prop, *obj = line.rstrip('\n.').split()
                obj = obj[0]
                subj = self.remove_prefix(subj)
                obj = self.remove_prefix(obj)
                prop_without_prefix = self.remove_prefix(prop)

                if prop_without_prefix in self.tables:

                    self.add_to_dict(subj, obj)
                    subj_int, obj_int = self.rdf_dict[subj], self.rdf_dict[obj]
                    self.tables[prop_without_prefix][obj_int].append(subj_int)


    def remove_prefix(self, s):
        """
        removes any prefixes in the watdiv data, for better readability.
        """

        if s[-1] == '>':
            s = s[: -1]
            for i, char in enumerate(s[::-1]):
                if not char.isdigit() and not char.isalpha():
                    return s[-i:]

        elif s[-1] == '"':
            return s

        else:
            return s[s.find(':') + 1:]


    def add_to_dict(self, subj, obj):
        """
        maps each subject and object to an unique integer
        """

        if subj not in self.rdf_dict:
            self.rdf_dict[subj] = len(self.rdf_dict) + 1
        if obj not in self.rdf_dict:
            self.rdf_dict[obj] = len(self.rdf_dict) + 1

    def reverse_rdf_dict(self):
        """
        reverse the initial rdf dict, so we can map each integer to the original 
        value for collecting the results
        """

        for key, value in self.rdf_dict.items():
            self.rdf_dict_reversed[value] = key
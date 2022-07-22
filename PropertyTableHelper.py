from collections import defaultdict

class PropertiesHelper:

    def __init__(self, file_path, dict_path, properties):

        self.tables = {property_name: defaultdict(list) for property_name in properties}
        self.rdf_dict = defaultdict()
        self.small_data = self.is_small_data(file_path)
        self.load_rdf_dict(dict_path)
        self.get_property_tables(file_path)


    def get_property_tables(self, file_path):
        """
        populates each property table with object being the key 
        and the corresponding subjects representing the values
        """
        with open (file_path, 'r') as file:

            for line in file:

                subj, prop, *obj = line.rstrip('\n.').split()
                obj = obj[0]
                prop_without_prefix = self.remove_prefix(prop)

                if prop_without_prefix in self.tables:

                    if self.small_data:
                        subj, obj = self.remove_prefix(subj), self.remove_prefix(obj)

                    subj_int, obj_int = self.rdf_dict[subj], self.rdf_dict[obj]
                    self.tables[prop_without_prefix][obj_int].append(subj_int)


    def is_small_data(self, file_path):
        """
        checks if we have to load the small, 100k, dataset or the bigger ones,
        because their formats differ
        """

        if 'M' in str(file_path):
            return False
        return True

    def remove_prefix(self, s):
        """
        removes any prefixes in the watdiv data, so that we can easily find the corresponding
        integer in the self.rdf_dict
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


    def load_rdf_dict(self, dict_path):
        """
        loads the provided dictionary, that maps each unique singlet of the RDF data
        to an integer. We remove the prefixes, so that we can also map the 100k
        data to an integer
        """

        with open (dict_path, 'r') as file:
            for line in file:
                key, value = line.rstrip('\n.').rsplit(':', 1)

                if self.small_data:
                    key = self.remove_prefix(key)

                self.rdf_dict[key]=int(value)
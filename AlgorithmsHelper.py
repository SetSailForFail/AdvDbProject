from collections import defaultdict

class Algorithm:

    def __init__(self, algo, yannakis, tables, output_file):
        """
        in this version of the algorithm, the property tables are in the form of
        object: array[subject]
        """

        self.tables = tables
        self.reverse_index(yannakis)
        self.file_name = output_file

        if algo == 'index_join':
            self.run_index_join()

        if algo == 'merge_join':
            self.run_merge_join()


    def reverse_index(self, yannakis):

        # reverse the index of oject_of_hasReview

        self.subjects_of_hasReview = defaultdict(set)
        for obj, subjects in self.tables['hasReview'].items():
            for subj in subjects:
                self.subjects_of_hasReview[subj].add(obj)

        # reverse the index of object_of_likes considering the relation
        # hasReview.subject = likes.object

        self.subjects_of_likes = defaultdict(set)
        for obj, subjects in self.tables['likes'].items():
            if yannakis:
                if obj in self.subjects_of_hasReview:
                    for subj in subjects:
                        self.subjects_of_likes[subj].add(obj)
            else:
                for subj in subjects:
                    self.subjects_of_likes[subj].add(obj)

        # reverse the index of object_of_friendOf considering the relation
        # likes.subject = friendOf.object

        self.subjects_of_friendOf = defaultdict(set)
        for obj, subjects in self.tables['friendOf'].items():
            if yannakis:
                if obj in self.subjects_of_likes:
                    for subj in subjects:
                        self.subjects_of_friendOf[subj].add(obj)
            else:
                for subj in subjects:
                    self.subjects_of_friendOf[subj].add(obj)

        # get the surviving objects of follows considering the relation
        # friendOf.subject = follows.object

        self.objects_of_follows = set()
        for obj, subjects in self.tables['follows'].items():
            if yannakis:
                if obj in self.subjects_of_friendOf:
                    self.objects_of_follows.add(obj)
            else:
                self.objects_of_follows.add(obj)


    def run_merge_join(self):
        """
        run a merge join on each intermediate computated result
        """


        # subjects of friendOf = objects of follows
        objects_of_friendsOf = self.merge_join(sorted(self.objects_of_follows), 
                                            sorted(self.subjects_of_friendOf.items(), key=lambda item: item[0]))

        # objects_of_friendsOf = subject of likes
        objects_of_likes = self.merge_join(sorted(objects_of_friendsOf), 
                                               sorted(self.subjects_of_likes.items(), key=lambda item: item[0]))

        # objects_of_likes = subjects_of_hasReview
        objects_of_hasReview = self.merge_join(sorted(objects_of_likes), 
                                              sorted(self.subjects_of_hasReview.items(), key=lambda item: item[0]))

        self.collect_result(objects_of_hasReview)


    def run_index_join(self):
        """
        run an index on each intermediate computated result
        """

        # subjects of friendOf = objects of followsf
        objects_of_friendsOf = {obj for followsObject in self.objects_of_follows 
                                    for obj in self.subjects_of_friendOf[followsObject]}

        # objects_of_friendsOf = subject of likes
        objects_of_likes = {obj for friendOfObjects in objects_of_friendsOf 
                                        for obj in self.subjects_of_likes[friendOfObjects]}

        # objects_of_likes = subjects_of_hasReview
        objects_of_hasReview = {obj for likesObject in objects_of_likes 
                                        for obj in self.subjects_of_hasReview[likesObject]}

        self.collect_result(objects_of_hasReview)


    def merge_join(self, objects, subjects_objects):
        
        result = set()
        i, j = 0, 0

        while i < len(objects) and j < len(subjects_objects):

            subj, obj = objects[i], subjects_objects[j][0]
            if subj == obj:
                result.update(subjects_objects[j][1])
                i += 1
                j += 1

            elif subj > obj:
                j += 1

            else:
                i += 1

        return result

    
    def collect_result(self, objects_of_hasReview):
        """
        here we are simply collecting each row and save the row to a file
        """
        
        generator = (
            (followsSubject, followsObject, friendOfObject, likesObject, hasReviewObject)
            for hasReviewObject in objects_of_hasReview 
            for likesObject in self.tables['hasReview'][hasReviewObject] 
            for friendOfObject in self.tables['likes'][likesObject] 
            for followsObject in self.tables['friendOf'][friendOfObject] 
            for followsSubject in self.tables['follows'][followsObject] 
        )

        with open(self.file_name, 'w') as file:
            for row in generator:
                file.write(str(row) + '\n')

Project 2 of Advanced Databases 

the main function, ```runQuery``` computes the result of the following query:

```
SELECT follows.subject, follows.object, friendOf.object, likes.object, hasReview.object
FROM follows, friendOf, likes, hasReview
WHERE follows.object = friendOf.subject
      AND friendOf.object = likes.subject
      AND likes.object = hasReview.subject
```

to achieve this, 4 arguments are required:

```
file_path: path to the watdiv dataset
algo: algorithm that should be used, can be either "index_join", or "merge_join" 
yannakis: can be set to True or False
output_file: name of the file where the result should be stored
```

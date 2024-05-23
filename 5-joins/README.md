# Joins

This was briefly touched already in exercise 3, but most often, information from one table is required in another table. Aside from the union (when you can directly merge the tables), another option to transfer information is the _join_ operation.

For these exercises, you will have the following extra tables on the measurements:

- Table of information on the veterinarians.
- Table of daily visitors.

## Task

Using these tables, answer the following questions :

- How many times has vet practice Digital Wildlife Care diagnosed a polar bear as sick?
- Which vet(s) has/have never seen a weight above the 99.9th percentile?
- Which vet was the least consistent in name capitalization?
- Which day had the lowest bear-to-visitor ratio? A bear can be seen if the vet determines the bear is healthy. (Hint: while joins require an exact match, this question is most easily solved using a non-exact match.)

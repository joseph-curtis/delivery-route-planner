_Author_ = "Joseph Curtis"
# Title:
# Description: 
# Inputs: 
# Outputs: 
# Date: 7 Apr 2023
# Sources: sololearn.com, stackoverflow.com, docs.python.org, w3schools.com/python

import utilities

test_hash = utilities.ChainingHashTable(5)
test_hash.insert(0, "zero")
test_hash.insert(1, "one")
test_hash.insert(2, "two")
test_hash.insert(3, "three")
test_hash.insert(4, "four")
test_hash.insert(5, "five")
test_hash.insert(6, "six")
test_hash.insert(7, "seven")
test_hash.insert(8, "eight")
test_hash.insert(9, "nine")
test_hash.insert(10, "ten")

for i in test_hash:
    print(i)
__author__ = "Joseph Curtis"
__license__ = "BSD 4-Clause"
__copyright__ = """Copyright 2023 Joseph Curtis 

 Licensed under the BSD 4-Clause License, (the “Original” or “Old” License);
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

  https://choosealicense.com/licenses/bsd-4-clause/

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations under
 the License.

 If you use this software, please cite it using the metadata from the
 CITATION.cff file.

"""
# Description: Data structures and misc. utility functions
# Date: 15 Mar 2023


class HashTableChained:
    """
    A Hash Table data structure using chaining

    Parameters
    ----------
    size : int
        The arg is used for ...

    Attributes
    ----------
    size : int
        The size of the hash table (default is 11).
        Note: this should be a prime number for more even bucket distribution
    hash_table : list
        The table that holds each bucket. Buckets contain tuples of key:value pairs.
    """
    # Constructor
    def __init__(self, size: int = 11):
        self.size = size
        self.hash_table = [[]] * self.size

    # when referencing this object, use just the hash_table variable
    def __repr__(self):
        return self.hash_table

    # String representation of the hash map items
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)

    def insert(self, key, value):
        """
        Add or update a new key/value pair into hash map

        Parameters
        ----------
        key :
            The key to index
        value :
            The data value

        Returns
        -------
        """
        # Get the hashed index from the key
        hashed_key = hash(key) % self.size
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        # search for an existing item with same key
        found_key = False
        for (index, record) in enumerate(bucket):
            (record_key, record_val) = record

            if record_key == key:
                found_key = True
                break

        # Update or append the new key/value pair to the bucket
        if found_key:
            bucket[index] = (key, value)
        else:
            bucket.append((key, value))

    def get_value(self, key):
        """
        Get a value associated with specific key

        Parameters
        ----------
        key :
            the index key to search

        Returns
        -------
        The value associated with given key, or None if not found.
        """
        # Get the hashed index from the key
        hashed_key = hash(key) % self.size
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        # search for the item using the key
        key_found = False
        for (index, record) in enumerate(bucket):
            (record_key, record_val) = record

            if record_key.equals(key) == key:
                key_found = True
                break

        # Return the value found,
        # or return None to indicate there was no record found
        if key_found:
            return record_val
        else:
            return None

    # Remove a value with specific key
    def remove(self, key):
        """
        Remove a record with matching key

        Parameters
        ----------
        key :
            The index key to search

        Returns
        -------

        """
        # Get the hashed index from the key
        hashed_key = hash(key) % self.size
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        # search for the item using the key
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            if record_key == key:
                found_key = True
                break

        if found_key:
            bucket.pop(index)   # delete the record
        return

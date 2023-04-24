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
# Date: 24 Apr 2023


class ChainingHashTable:
    """
    A Hash Table data structure using chaining

    Parameters
    ----------
    bucket_number : int
        Defines how large the hash table is (how many buckets it will have)

    Attributes
    ----------
    bucket_number : int
        The size of the hash table (default is 31).
        Note: this should be a prime number for more even bucket distribution
    hash_table : list
        The table that holds each bucket. Buckets contain tuples of key:value pairs.
    """

    def __init__(self, bucket_number: int = 31):
        self.bucket_number = bucket_number
        self.hash_table = [[] for _ in range(self.bucket_number)]

    def __iter__(self):  # make this object iterable
        return ChainingHashTableIter(self)

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
        hashed_key = hash(key) % self.bucket_number
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

    def get(self, key):
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
        hashed_key = hash(key) % self.bucket_number
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        # search for the item using the key
        key_found = False
        for (index, record) in enumerate(bucket):
            (record_key, record_val) = record

            if record_key == key:
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
        hashed_key = hash(key) % self.bucket_number
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
            bucket.pop(index)  # delete the record
        return


class ChainingHashTableIter:
    """
    A Hash Table data structure using chaining

    Parameters
    ----------
    chaining_hash_table : ChainingHashTable
        The parent object calling this iterator

    Attributes
    ----------
    _hash_table :
        The chaining hash table to iterate over
    _current_bucket : int
        The current bucket iterator is searching in
    _current_item : int
        Index of current item pointed to
    """

    def __init__(self, chaining_hash_table: ChainingHashTable):
        self._hash_table = chaining_hash_table.hash_table
        self._current_bucket = 0
        self._current_item = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._current_bucket < len(self._hash_table):
            if self._current_item < len(self._hash_table[self._current_bucket]):
                result = self._hash_table[self._current_bucket][self._current_item]
                self._current_item += 1
                return result
            else:
                self._current_bucket += 1
                self._current_item = 0

        raise StopIteration

